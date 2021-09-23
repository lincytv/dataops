#!/bin/bash -xe
sudo apt-get update -qq

# Needed for jekyll
sudo apt-get -y install ruby ruby-dev make build-essential nodejs python yamllint jsonlint

# Needed for html-proofer
sudo apt-get -y install curl libc6 libcurl4 zlib1g
sudo apt-get -y install libxml2-dev libxslt-dev

# Install jekyll

# --no-ri --no-rdoc deprecated use --no-document instead
# https://github.com/rubygems/heroku-buildpack-bundler2/pull/1
gem install -V jekyll-gist --no-document
gem install -V jekyll --no-document

# Install html-proofer
gem install -V nokogiri -- --use-system-libraries --with-xml2-include=/usr/include/libxml2 --no-document
gem install -V html-proofer --no-document

# Install ymallint
gem install -V yamllint --no-document

# Install jsonlint
gem install -V jsonlint --no-document

pwd
