There are three steps to installing this application
1. Install the Scoreboard system (aka ctfd.io)
1. Install the buggy website that students will attack (aka The Juice Shop Challenges)
1. Import into the Scoreboard the information about each of the bugs for users to choose a challenge.

* This guide assumes you are instllating into a newly installed Debian based ditro such as Ubuntu.
* The repository contains both the setup guide (the ReadMe you are reading now) and the actual software for the installation. 

# Clone the Repo to your new Linux box.
```
sudo apt-get install git net-tools
git clone https://github.com/UKNorthernlad/juiceboxctf/
cd juicebox
```

# The Scoreboard
ctfd.io is a platform for keeping the scope for Capture The Flag type events. Once installed you can install separate standalone challenges which run in their own docker containers.

## Install Required packages and signing keys for Docker
```
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
```

## Install Docker & run test container
```
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
```

## Download Docker Compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Pre-pull all the images needed
These aren't really needed here as docker-compose will do it for us if we ommit them here.
```
sudo docker pull nginx:stable
sudo docker pull mariadb:10.4.12
sudo docker pull redis:4
sudo docker pull bkimminich/juice-shop
```

## Create a secret key
This is used as a salt for the generated flags to make them unique to this installation.
```
head -c 64 /dev/urandom > .ctfd_secret_key
```

## Start the service up in "interactive" mode
This will allow you to watch all the output & errors from the containers in real time.
```
sudo docker-compose up
```
> Wait about 5 minutes as it takes time for the various containers to start and for database tables and caches to be initialized and for the nginx proxy to start.
> 
> Once complete, should now be able to access the Scoreboard service on http://localhost:8000
> 
> The result should look like this:

![Screenshot showing Initial Setup ](/images/setup.png 'Initial Setup')

## Configure the Service
* Enter an "Event Name" of "Training".
* For "Mode" choose "User"
* For "Administration" enter "admin" for the username, "admin@admin.admin" for the email & "admin" for the password.

> Configuration of the scoreboard ctfd is now complete. Move onto Install the "Juice Shop".

## The following are useful if you need to reset the score system 
### Stop the service
* A simple ctrl-C in the terminal from where you ran "docker-compose up" will stop all containers.
* Use "docker-compose up" to re-start everything again.
* As an alternative from another window: `docker-compose down`

### Reset the application back to this point
If you ever need to reset the scoreboard environment right back to the beginning, run the following from the "ctfd" directory:
```
docker-compose down
docker rm -f $(docker ps -a -q)
docker volume prune
rmdir .data
```

# Install the "Juice Shop"
This is a set of hacking challenges which target the OWASP Top 10 vulnerabilities. It's the world's most modern yet insecure website!
Reference - https://owasp.org/www-project-juice-shop/
Reference - https://pwning.owasp-juice.shop/
Reference - Answers to challenges -> https://www.youtube.com/watch?v=AIUhCdOMrmc

## Download the docker image.
This is a pre-build image of the main content at https://github.com/juice-shop/juice-shop
```
docker pull bkimminich/juice-shop
```

## Run the image
```
docker run --rm -e "NODE_ENV=ctf" -p 3000:3000 bkimminich/juice-shop
```
> Open a browser to http://localhost:3000 to view the site.

# Import the Challenge definition
* This will import the .zip file created previously into the Scoreboard system.
* It contains the information about all the bugs in the Juice Shop site.
* Provides a menu of different challenges to select from inside the scoreboard system - the only downside the challenges don't have URLs provided :( 
* Reference - https://github.com/juice-shop/juice-shop-ctf

```
apt-get install -y npm
npm install -g juice-shop-ctf-cli
```

## Run the application
Accept the default options for the first 3 questions (CTFd, JuiceShopURL, SecretKey) then choose the "Free" option for the next three.
```
juice-shop-cli
```

> Once completed, you will file a file called "OWASP_Juice_Shop.xxxx-xx-xx.CTFd.zip" in the local folder.

![Screenshot showing generation of config .zip file ](/images/generatezipfile.png 'Challanges .zip file creation')

* Open the browser to the ctfd homepage, then browse to Config ->  Backup -> Import and select .zip file created above. 
 
* Once the data is imported, you should see the following:

![Screenshot showing imported challenged](/images/importedchallenges.png 'Imported challenges')

# References
* https://docs.ctfd.io/docs/deployment/installation
* Setup Guide for AWS - https://www.doyler.net/security-not-included/owasp-juice-shop-ctfd
