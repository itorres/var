build: cmu
	docker build --network host -t 127.0.0.1:5000/itorres/k8s-abuse:latest .

push: build
	docker push 127.0.0.1:5000/itorres/k8s-abuse:latest

.PHONY: all build serve shell ipython
cmu:
	curl -Ls https://github.com/itorres/var/releases/download/cmu-0.1/cmu.tgz | tar xzf -
serve:
	docker run -it --net=host 127.0.0.1:5000/itorres/k8s-abuse:latest
shell: 
	docker run -it --net=host 127.0.0.1:5000/itorres/k8s-abuse:latest bash
ipython:
	docker run -it --net=host 127.0.0.1:5000/itorres/k8s-abuse:latest ipython
