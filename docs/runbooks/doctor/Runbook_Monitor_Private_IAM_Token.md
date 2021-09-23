---
layout: default
description: Runbook Pirvate IAM Token Error
title: RETIRED Runbook Pirvate IAM Token Error
service: doctor_private_iam_oidc_token
runbook-name: Runbook Pirvate IAM Token Error
tags: oss, private_iam_token, doctor, doctor_private_iam
link: /doctor/Runbook_Monitor_Private_IAM_Token.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert will be triggered if the Doctor private iam failed to get token by apikey, monitored by New Relic.

## Technical Details

The reason for this alert could be one of the following:
  1. The Cert expiration.
  

## User Impact

Users who are using the private iam token changed by apikey will be affected.

## Instructions to Fix


1. Double check the URL status:

   ```
   curl -H "Content-Type: application/x-www-form-urlencoded" -u bx:bx -X POST -d "apikey=<ApiKey>&grant_type=urn:ibm:params:oauth:grant-type:apikey" "https://iam.oss.cloud.ibm.com:8999/oidc/token"
   ```
   > **Notes:**
    * Replace the `<ApiKey>` with your own api key, you can get it from [{{doctor-portal-name}} profile info]({{doctor-portal-link}}/#/profile/info) for [more info about ApiKey]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html)
    

2. If it return 
```
{"access_token":"****","refresh_token":"****","token_type":"Bearer","expires_in":3600,"expiration":<A NUBER>}
```
then you can resolve the alert. 
   
3. If return 
```
{"context":{"requestId":"<A NUBER>","requestType":"incoming.OIDC_Token","userAgent":"curl/7.64.1","clientIp":"<IP>","instanceId":"jobname/0","threadId":"<A NUBER>","host":"ossbus2","startTime":"<TIME> UTC","endTime":"<TIME> UTC","elapsedTime":"<A NUBER>","locale":"en_US"},"errorCode":"BXNIM0415E","errorMessage":"Provided API key could not be found","errorDetails":"BXNIM0102E: Unable to find Object. Object Type: 'ApiKey' with ID: '<APIKEY>' not found."}
```
your apikey is wrong.
   
4. If return 
```
{"context":{"requestId":"<A NUBER>","requestType":"incoming.OIDC_Token","userAgent":"curl/7.35.0","clientIp":"0:0:0:0:0:0:0:1","instanceId":"jobname/0","threadId":"<A NUBER>","host":"doctormbus3","startTime":"<TIME> UTC","endTime":"<TIME> UTC","elapsedTime":"<A NUBER>","locale":"en_US"},"errorCode":"BXNIM0050E","errorMessage":"javax.net.ssl.SSLHandshakeException: SSLHandshakeException invoking https://uaa.stage1.ng.bluemix.net/oauth/token: java.security.cert.CertificateException: PKIXCertPathBuilderImpl could not build a valid CertPath.","errorDetails":"SSLHandshakeException invoking https://uaa.stage1.ng.bluemix.net/oauth/token: java.security.cert.CertificateException: PKIXCertPathBuilderImpl could not build a valid CertPath."}
```
it means cert problem, follow the [Guide](https://www.ibm.com/support/knowledgecenter/SSEQTP_liberty/com.ibm.websphere.wlp.doc/ae/twlp_add_trust_cert.html).
  
  + 4-1 Exception Message from Liberty. On path: /logs/, will see some exception:
  
   ```
/20/20 18:11:27:666 UTC] 00001a22 com.ibm.ws.ssl.core.WSX509TrustManager                       E CWPKI0022E: SSL HANDSHAKE FAILURE:  A signer with SubjectDN CN=wil
dcard.stage1.ng.bluemix.net, O=International Business Machines Corporation, L=Armonk, ST=New York, C=US was sent from the target host.  The signer might need to be added to local trust store /opt/ibm/wlp/usr/servers/defaultServer/trustedCertificates.jks, located in SSL configuration alias defaultSSLConfig.  The extended error message from the SSL handshake exception is: PKIX path building failed: java.security.cert.CertPathBuilderException: PKIXCertPathBuilderImpl could not build a valid CertPath.; internal cause is: 
        java.security.cert.CertPathValidatorException: The certificate issued by CN=DigiCert Global Root CA, OU=www.digicert.com, O=DigiCert Inc, C=US is not trusted; internal cause is: 
        java.security.cert.CertPathValidatorException: Certificate chaining error
[2/20/20 18:11:27:666 UTC] 00001a22 .ibm.ws.jaxrs.2.0.common:1.0.20.cl180120180309-2209(id=180)] W Interceptor for {https://uaa.stage1.ng.bluemix.net/oauth/token}WebClient has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: Could not send Message.
        at org.apache.cxf.interceptor.MessageSenderInterceptor$MessageSenderEndingInterceptor.handleMessage(MessageSenderInterceptor.java:64)
        ......
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635)
        at java.lang.Thread.run(Thread.java:811)
Caused by: javax.net.ssl.SSLHandshakeException: SSLHandshakeException invoking https://uaa.stage1.ng.bluemix.net/oauth/token: java.security.cert.CertificateException: PKIXCertPathBuilderImpl could not build a valid CertPath.
        at sun.reflect.GeneratedConstructorAccessor62.newInstance(Unknown Source)
        ... 82 more
Caused by: javax.net.ssl.SSLHandshakeException: java.security.cert.CertificateException: PKIXCertPathBuilderImpl could not build a valid CertPath.
        at com.ibm.jsse2.k.a(k.java:15)
        ......
        ... 85 more
Caused by: java.security.cert.CertificateException: PKIXCertPathBuilderImpl could not build a valid CertPath.
        at com.ibm.ws.ssl.core.WSX509TrustManager.checkServerTrusted(WSX509TrustManager.java:322)
        at com.ibm.jsse2.aB.checkServerTrusted(aB.java:35)
        at com.ibm.jsse2.E.a(E.java:831)
        ... 104 more
```
  + 4-2 Follow [Guide](https://www.ibm.com/support/knowledgecenter/SSEQTP_liberty/com.ibm.websphere.wlp.doc/ae/twlp_add_trust_cert.html) before.
  + 4-3 Steps to fix
  ```
root@doctormbus3:/opt/ibm/wlp/usr/servers/defaultServer# echo q | openssl s_client -showcerts -connect uaa.stage1.ng.bluemix.net:443
CONNECTED(00000003)
depth=2 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Global Root CA
verify return:1
depth=1 C = US, O = DigiCert Inc, OU = www.digicert.com, CN = DigiCert Secure Site ECC CA-1
verify return:1
depth=0 C = US, ST = New York, L = Armonk, O = International Business Machines Corporation, CN = wildcard.stage1.ng.bluemix.net
verify return:1
---
Certificate chain
 0 s:/C=US/ST=New York/L=Armonk/O=International Business Machines Corporation/CN=wildcard.stage1.ng.bluemix.net
   i:/C=US/O=DigiCert Inc/OU=www.digicert.com/CN=DigiCert Secure Site ECC CA-1
-----BEGIN CERTIFICATE-----
MIIOuDCCDl6gAwIBAgIQBHA4W/WJpHA3rlnamm8j/jAKBggqhkjOPQQDAjBnMQsw
......
AwIDSAAwRQIhALJvE7Z749zpyRkBrVIPgHE+SKHuT5GOrN+Q3lQZNm4JAiBK/JQd
LXm5r1ZVmupzU/30Eyvh744oNsQDjccZLixqxQ==
-----END CERTIFICATE-----
 1 s:/C=US/O=DigiCert Inc/OU=www.digicert.com/CN=DigiCert Secure Site ECC CA-1
   i:/C=US/O=DigiCert Inc/OU=www.digicert.com/CN=DigiCert Global Root CA
-----BEGIN CERTIFICATE-----
MIIDyTCCArGgAwIBAgIQC1v2W2un+9CLKQ2QRTfe4DANBgkqhkiG9w0BAQsFADBh
......
eyiYwvPQIUJ9ODieH5vDzLq9XvtdmFzBPXlFnHKI9LphN6sUVXdf4B+dao9drFZE
ifuXbKlQ/2TRZPFeBg==
-----END CERTIFICATE-----
---
Server certificate
Y2xvdWQuaWJtLmNvbYIaYXBpLnJtYy50ZXN0LmNsb3VkLmlibS5jb22CHSouYWNj
subject=/C=US/ST=New York/L=Armonk/O=International Business Machines Corporation/CN=wildcard.stage1.ng.bluemix.net
issuer=/C=US/O=DigiCert Inc/OU=www.digicert.com/CN=DigiCert Secure Site ECC CA-1
---
No client certificate CA names sent
Peer signing digest: SHA256
Server Temp Key: ECDH, P-256, 256 bits
---
SSL handshake has read 5217 bytes and written 431 bytes
---
New, TLSv1/SSLv3, Cipher is ECDHE-ECDSA-AES256-GCM-SHA384
Server public key is 256 bit
Secure Renegotiation IS supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-ECDSA-AES256-GCM-SHA384
    Session-ID: 41BFABA8AABD6E523768FFD6A45C3901E592CC525666B115E4B6963BC4DBAC85
    Session-ID-ctx: 
    Master-Key: 40AC70651D5B6BE269B2D74ED6C73198FD8AA6365B970E4FEB13FD2CED199DDA70E22340F071CD90B910768D15A10920
    Key-Arg   : None
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 00 00 35 90 34 cd 38 44-34 da d7 e0 56 f6 e9 de   ..5.4.8D4...V...
    ......
    0090 - bd df e2 83 cf 19 68 09-06 6e 38 96 31 9d 07 b8   ......h..n8.1...
    Start Time: 1582254702
    Timeout   : 300 (sec)
    Verify return code: 0 (ok)
---
DONE
```
Then save FIRST cert to c.cer, and run following command to import the cert file to the `./trustedCertificates.jks`
in liberty's server folder: /opt/ibm/wlp/usr/servers/defaultServer
```
root@doctormbus3:/opt/ibm/wlp/usr/servers/defaultServer# keytool -importcert \
     -file ./c.cer \
     -alias stage1_cert \
     -keystore ./trustedCertificates.jks \
     -storepass changeit \
     -storetype jks
root@doctormbus3:/opt/ibm/wlp/usr/servers/defaultServer# ls -l
total 88
drwxr-x--- 2 root root  4096 May 23  2018 apps
-rw-r--r-- 1 root root    93 May  5  2017 bootstrap.properties
-rw-r--r-- 1 root root  5165 Feb 21 03:25 c.cer
-rw-r--r-- 1 root root  3840 Feb 21 03:43 defaultTrustStore
drwxr-x--- 2 root root  4096 May 11  2018 dropins
-rw-r--r-- 1 root root   114 Jun 23  2017 server.env
-rw-r--r-- 1 root root  8355 May 23  2019 server.xml
-rw-r--r-- 1 root root 17811 Feb 21 03:23 trustedCertificates.jks
-rw-r--r-- 1 root root 17811 Jun 29  2017 trustedCertificates.jks.backup
-rw-r--r-- 1 root root   112 May  5  2017 userfile.properties
-rw-r--r-- 1 root root    22 May  5  2017 userfile_exclusive.properties
```
   Then exit the container and restart the `doctor_iam` container.
  + 4-4 Verify with step 1
  
5. Other result or helps contact shanec@ca.ibm.com in NA's timezone.
