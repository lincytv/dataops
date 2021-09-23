---
layout: default
description: Setting up the vault and consul server
title: Step by step to set up Vault service
service: backend
runbook-name: Step by Step Set Up Vault Service
tags: doctor,backend
link: /doctor/Runbook_Step_By_Step_Set_Up_Vault_Service.html
type: Informational
---

## To setup one vault and consul server

### 1. Set up the consul backend

`docker run -d -P --name=consul1 consul:0.9.0 agent -server -bootstrap -ui -disable-host-node-id -client 0.0.0.0`  

### 2. Edit the vault configure file  
`vim /etc/vault/vault.hcl`  

For the following, replace the `8500` with the corresponding export port in host:

storage "consul" {  
  address = "0.0.0.0:8500"  
  path    = "vault"  
}  
listener "tcp" {  
  address     = "0.0.0.0:8200"  
  tls_disable = 1  
}  

### 3. Set up the vault  
`wget https://releases.hashicorp.com/vault/0.7.3/vault_0.7.3_linux_amd64.zip`  
`unzip vault_0.7.3_linux_amd64.zip`  
`cp vault /usr/bin/`
`vault server -config=/etc/vaultvault.hcl`  

## Set up one vault and consul cluster (3 nodes)
### 1. Set up the consul cluster (the configure file in the Doctor-go repo)

## Notes and Special Considerations
   {% include {{site.target}}/tips_and_techniques.html %}
