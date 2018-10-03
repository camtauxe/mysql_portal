rsync -avh --progress=info2 -e ssh ./deploy/ friend@camerontauxe.com:/srv/cs482teamsite/
ssh friend@camerontauxe.com chmod 775 /srv/cs482teamsite/*.py /srv/cs482teamsite/lib/*.py
