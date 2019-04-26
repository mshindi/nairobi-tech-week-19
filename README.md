# nairobi-tech-week-19
Repo for Nairobi Tech Week workshop - "Moving from a monolithic architecture to a microservices architecture"

## Medium articles
Microservices at Twiga - https://medium.com/twigatech/microservices-at-twiga-part-1-aa0bea4f356b

Microservices at Twiga — Design, Technology & Infrastructure - https://medium.com/twigatech/microservices-at-twiga-design-technology-infrastructure-848622c86dcd

Clone the repo and cd into the working folder using the command bellow

```
git clone https://github.com/mshindi/nairobi-tech-week-19.git && cd nairobi-tech-week-19
```

cd into the nameko directory and create the virtualenv
```
virtualenv env
```
or
```
virtualenv env -p3
```

activate the env

```
source env/bin/activate
```

Install the python requiremtns 
```
pip install -r requirements.txt
```

Install the node requirements
```
cd nameko && cd movie && npm i
```

Make sure you have rabbitmq installed - https://www.rabbitmq.com/

Then start it
Mac os
```
/usr/local/sbin/rabbitmq-server
```

Run the nameko services

Location service
```
cd location/ && ./run.sh
```

Schedule service
```
cd schedule/ && ./run.sh
```

Movie service
```
cd movie/ && npm run start
```