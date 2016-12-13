{
  network.description = "EFK network";
  network.enableRollback = true;

  elasticsearch =
    { config, pkgs, ... }:
    with pkgs.lib;

    { networking.hostName = "elasticsearch";
      networking.firewall = {
        allowPing = true;
        allowedTCPPorts = [ 9200 ];
      };
      services.elasticsearch.enable = true;
      services.elasticsearch.listenAddress = "0.0.0.0";
    };

  kibana =
    { config, pkgs, nodes, ... }:
    with pkgs.lib;

    { networking.hostName = "kibana";
      networking.firewall = {
        allowPing = true;
        allowedTCPPorts = [ 5601 ];
      };
      networking.extraHosts = ''
      ${nodes.elasticsearch.config.networking.privateIPv4} elasticsearch
      '';
      services.kibana.enable = true;
      services.kibana.listenAddress = "0.0.0.0";
      services.kibana.elasticsearch.url = "http://elasticsearch:9200";
    };

  webserver =
    { config, pkgs, nodes, ... }:
    with pkgs.lib;

    let

      webRoot = pkgs.stdenv.mkDerivation rec {
        name= "webroot-1.0";

        builder = let
          index = builtins.toFile "index.html" "
<html>
<head>
  <title>NixOps Demo</title>
</head>
<body>
  <h1>Hello world!</h1>
</body>
</html>
         ";
        in builtins.toFile "builder.sh" "
            source $stdenv/setup
            mkdir $out
            cp ${index} $out/index.html
            echo frita > $out/patata
        ";
      };

    in
    { networking.hostName = "webserver";
      networking.firewall = {
        allowPing = true;
        allowedTCPPorts = [ 80 443 ];
      };
      networking.extraHosts = ''
      ${nodes.elasticsearch.config.networking.privateIPv4} elasticsearch
      '';
      services.nginx.enable = true;
      services.nginx.config = ''
      events {}
      http {
        include ${pkgs.nginx}/conf/mime.types;
        error_log /tmp/nginx_error.log;
        access_log /tmp/nginx_access.log;
        server {
          listen 80 default_server;
          server_name default_server;
          root ${webRoot};
        }
      }
      '';
      services.fluentd.enable = true;
      services.fluentd.config = ''
        <source>
          @type tail
          @label nginx
          read_from_head true
          path /tmp/nginx_access.log
          pos_file /tmp/nginx_access.log.pos
          format nginx
          tag nginx
        </source>
        <label @nginx>
          <match **>
            @type elasticsearch
            logstash_format true
            host elasticsearch
            logstash_prefix nginx
            flush_interval 5s
          </match>
        </label>
      '';
    };
}
