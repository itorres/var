let

  config =
    { deployment.targetEnv = "libvirtd";
      deployment.libvirtd.headless = true;
    };

in

{
  elasticsearch = config;
  kibana = config;
  webserver = config;
}
