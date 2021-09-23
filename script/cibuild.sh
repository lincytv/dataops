#!/bin/bash -xe
sudo apt-get update -qq

# Needed for jekyll
sudo apt-get -y install ruby-dev build-essential nodejs python

# Needed for html-proofer
sudo apt-get -y install curl libc6 libcurl3 zlib1g
sudo apt-get -y install libxml2-dev libxslt-dev

# Install jekyll
gem install -V jekyll-gist -v 1.3.0 --no-ri --no-rdoc
gem install -V jekyll -v 2.5.3 --no-ri --no-rdoc

# Install html-proofer
gem install -V nokogiri -- --use-system-libraries --with-xml2-include=/usr/include/libxml2 --no-ri --no-rdoc
gem install -V html-proofer -v 2.5.2 --no-ri --no-rdoc

# Install jsonlint
sudo npm install jsonlint -g


pwd

# Generate the html site ready for validation
jekyll build --verbose --destination ./_site

# Validate the generated html
htmlproof --verbose --disable-external --empty-alt-ignore --href-ignore "/#.*/","/\/executive/"  --file-ignore "/view.html$/" ./_site

# Check all the json files are valid
# find with xargs so that the return code can be used
#jsonlint isn't validating. Error: unknown argument '-V'. No options available for command.
find ./_site -name '*.json' -print0 | xargs -0 -I '{}' sh -c 'echo {} ; jsonlint {}'
