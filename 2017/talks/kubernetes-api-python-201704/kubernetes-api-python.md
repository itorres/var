
class: center, middle

# Smashing the K8s API for fun and profit

![Kubernetes Logo](k8s.png)

## Python edition

Ignacio Torres Masdeu  
<https://itorres.net>

---

# A quick travel down memory lane

Founded by [Joe Beda][], [Brendan Burns][] and [Craig McLuckie][] who
were quickly joined by other Google engineers
including [Brian Grant][] and [Tim Hockin][] and was first announced
by Google in mid-2014. ([Source: Wikipedia][])

[Source: Wikipedia]: https://en.wikipedia.org/wiki/Kubernetes
[Joe Beda]: https://github.com/jbeda
[Brendan Burns]: https://github.com/brendandburns
[Craig McLuckie]: https://twitter.com/cmcluck
[Tim Hockin]: https://github.com/thockin
[Brian Grant]: https://github.com/bgrant0607

#### Further reading
- [Interview with Eric Brewer][brewer]. Medium S-C-A-L-E May 2015
- https://www.wired.com/2015/06/google-kubernetes-says-future-cloud-computing/
- Brendan Burns, Brian Grant, David Oppenheimer, Eric Brewer, and
  John Wilkes. 2016. Borg, Omega, and Kubernetes. Commun. ACM 59, 5
  (April 2016), 50-57. DOI: https://doi.org/10.1145/2890784
- Abhishek Verma, Luis Pedrosa, Madhukar Korupolu, David Oppenheimer,
  Eric Tune, and John Wilkes. 2015. Large-scale cluster management at
  Google with Borg. In Proceedings of the Tenth European Conference on
  Computer Systems (EuroSys '15). ACM, New York, NY, USA, , Article 18
  , 17 pages. DOI: https://doi.org/10.1145/2741948.2741964

[brewer]: https://medium.com/s-c-a-l-e/google-systems-guru-explains-why-containers-are-the-future-of-computing-87922af2cf95
[wired]: https://www.wired.com/2015/06/google-kubernetes-says-future-cloud-computing/
[wilkes]: https://www.wired.com/2013/04/google-john-wilkes-new-hackers/

---

# What's in a name
   Kubernetes _(from κυβερνήτης: Greek for "helmsman" or "pilot")_.

   Its development and design are heavily influenced by Google's Borg
   system, and many of the top contributors to the project previously
   worked on Borg.

   The original name for Kubernetes within Google was project _Seven
   of Nine_, a reference to a _Star Trek™_ character that is a
   'friendlier' Borg.

   Using trade marks in software projects is a _bad idea™_, just ask
   [Bryan Cantrill][] about Sun's [Project _Kevlar™_][kevlar].

   [Bryan Cantrill]: https://github.com/bcantrill
   [kevlar]: https://youtu.be/-zRN7XLCRhc?t=13m29s

   The seven spokes on the wheel of the Kubernetes logo is a small
   acknowledgment of Kubernetes' original name.
            
---

# What Kubernetes provides

More than a _container orchestrator_.

- Deployment management
  - Single command rollouts, rollbacks and scaling
  - Optionally automated
  - Declarative
- Resource management
  - CPU
  - Memory
- Storage orchestration
  - Provision and management of volumes
  - Storage abstraction

---

# How Kubernetes provides it

Modular, every component is pluggable.

  - [Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
      - Flannel
      - Weave
      - Calico
  - [Storage](https://kubernetes.io/docs/concepts/storage/volumes/)
      - GCEPersistentDisk, AWSElasticBlockStore, AzureFile and AzureDisk
      - Ceph (RBD and CephFS), Glusterfs
      - iSCSI, FC, NFS
      - emptyDir, gitRepo, secret, downwardAPI
  - Container runtime
      - Docker
      - [rkt](https://kubernetes.io/docs/getting-started-guides/rkt/)
        (important caveats)
      - [cri-o](https://github.com/kubernetes-incubator/cri-o) (pre-alpha)

Portable

  - The same manifests can be applied on GCE, AWS or bare
    metal with minimum changes.

---

# Setup Kubernetes on your laptop

Just add these lines to your [`configuration.nix`][] and run
`nixos-rebuild switch`.

```nix
  networking.bridges.cbr0.interfaces = [];
  networking.interfaces.cbr0 = {};
  networking.firewall.trustedInterfaces = ["cbr0"];
  networking.nat.enable = true;
  networking.nat.externalInterface = "+";
  networking.nat.internalInterfaces = ["cbr0"];
  
  services.kubernetes.roles = ["master" "node"];
  services.kubernetes.verbose = true;
  virtualisation.docker.extraOptions = "--iptables=false --ip-masq=false -b cbr0";
```
[`configuration.nix`]: https://github.com/xtruder/nix-profiles/blob/master/profiles/kubernetes.nix

--
count:false
Because you're using [NixOS](https://nixos.org/), right?

--
count:false

If not, [minikube][] will probably rock your boat.

[minikube]: https://github.com/kubernetes/minikube

---

# Setup: Local registry
We need a place to push our local images to.

https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/registry

Convoluted due to Docker's "insecure registry" logic. Registries must
be accessed through TLS except for `localhost` so we set up:

- A registry `Pod` with a `PersistentVolumeClaim`.
- A `ClusterIP` `Service` pointing internal requests to the registry
  `Pod`.
- A `DaemonSet` that spawns a proxy `Pod` on every node so the local Docker
  daemon can pull the images from `localhost`.

--
count:false

Obviously. [I think that's pretty obvious][wat].

[wat]: https://www.destroyallsoftware.com/talks/wat

--

Anyway now we are able to build push to our registry our images:

```sh
docker push 127.0.0.1:5000/itorres/k8s-abuse:latest
docker build -t 127.0.0.1:5000/itorres/k8s-abuse:latest .
```

---

# The kubernetes API

Kubernetes objects are representations of our system.
- [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Volume](https://kubernetes.io/docs/concepts/storage/volumes/)
- [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

`kubectl` is an API interface that allows us to do CRUD operations on
our system.

---

# The kubernetes API

--
count:false

Guess what. 
--
count:false

```sh
gaia:~$ kubectl get deploy nginx -o yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  creationTimestamp: 2017-04-02T22:52:28Z
  generation: 1
  labels:
    run: nginx
  name: nginx
  namespace: default
  resourceVersion: "13649"
  selfLink: /apis/extensions/v1beta1/namespaces/default/deployments/nginx
  uid: 0c366655-17f7-11e7-815c-441ca8e14c29
spec:
  replicas: 1
  selector:
    matchLabels:
      run: nginx
```

You are already using it.

---

# The kubernetes API

Several interfaces

- kubectl
- A library for your favourite language
- REST API

In the end all of them use the REST API.

---

# `kubectl`: love it
```sh
$ kubectl --context local get service nginx
NAME      CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
nginx     10.10.10.131   <nodes>       80/TCP    42s
```

---

# `kubectl`: or hate it
```sh
$ kubectl --context local describe service nginx
Name:			nginx
Namespace:		default
Labels:			pod-template-hash=701339712
			run=nginx
Selector:		pod-template-hash=701339712,run=nginx
Type:			NodePort
IP:			10.10.10.131
Port:			<unset>	80/TCP
NodePort:		<unset>	30220/TCP
Endpoints:		10.10.0.3:80
Session Affinity:	None
```

Use jsonpath ASAP.

---

# `kubectl` with `-o jsonpath`

Interactively explore the objects with [jid][]. Check this [gist][]
for more kubectl output

```sh
kubectl get no -o json | jid -q | pbcopy
```

[jid]: https://github.com/simeji/jid
[gist]: https://gist.github.com/so0k/42313dbb3b547a0f51a547bb968696ba

--
count:false

```sh
$ kubectl --context local get services -o \
  jsonpath="{.items[?(@.spec.ports[*].nodePort)].metadata.name}\
  {.items[*].spec.ports[*].nodePort}:"|tr : "\n"

nginx 30220
```
--
count:false

Better, but still far from perfect
- jsonpath is only available on `get` operations.
- But there is a lot of info only available through the `kubectl
  describe`.
- We need to do a lot of things and pipes get you far, but not so
  much.
  
---

# Our use case

Need to support different environments
- GCE
- AWS
- Bare metal

We're already deploying in GCE
```
gaia:~$ kubectl --context cloud get service --all-namespaces -o name | wc -l
92
gaia:~$ kubectl --context cloud get pod --all-namespaces -o name | wc -l
301
```

And that grows every week.

---

class: center, middle
# Demo Time

![Shake it](shake-it.gif)

