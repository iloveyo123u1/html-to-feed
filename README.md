# html-to-feed
A generator that creates RSS feeds from any HTML site based on a set of rules

For testing it in a `virtualenv` do the following:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements
python website.py
```

Then view the source code of `http://127.0.0.1:5000/feed/1`.

Using the `Dockerfile` you can also create a docker image

```bash
docker build .
```

and then access the website via the docker image. Find out the IP with:

```bash
docker inspect $CONTAINER_NAME | grep IPAddress
```
