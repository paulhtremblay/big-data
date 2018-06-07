Attachment personal.jpg added.
Conversation opened. 3 messages. All messages read.

Skip to content
Using Gmail with screen readers
Your conversation has been added to the task list
4 of 5,150
 
FW: login info for DSVM
Inbox
  x
  Chad Sleeman <sleeman1@uw.edu>
    
  May 18 (1 day ago)
    
  to IELP, me, Brendan, Cheryl, Rudy, Paul

  I set up azure access to a DSVM for you. Below are instructions that should help you connect to the DSVM with X2go. You can also use SSH and find the connection info listed on the VM in azure under IP address or FQDN.

   

  If you have questions let me know.

   

  -Chad

   

   

   

  OK, I was able to get Jupyter access from a DevTest DSVM but I had to rebuild the lab environment enabling a public IP for each VM to do so.  Below are step by step instructions.

   

  1.       Log into http://Portal.Azure.com using your uwzwu@uw.edu account

  2.       Click on All Resources and in “Filter By Name” Type Deep_Learning

  3.       Click on the Deep_Learning DevTest resource.

  4.       Near the top middle of the screen click on “Claim any” this will claim a random DSVM of the pool of 5 I have set up. The claim process may take 30+ seconds. (I have had it take well over a minute as Azure is also starting up the VM.)

  5.       After the DSVM is claimed it should show up under “My virtual machines” in the Deep_learning panel. Click on the DSVM in My virtual machines.

   

  The new user name and password for all of the DSVM’s: UWStudent  PW: UW3tudent

   

  Here access to the DSVM can fork depending on the need.

   

  You can SSH into the DSVM using Putty and the FQDN provided by azure, located in the information about the DSVM you claimed.

   

  OR

   

  You can download X2GO https://wiki.x2go.org/doku.php and connect to the GUI using the FQDN.  In X2GO will need to select XFCE under session type.

   

   

  Jupyter is accessible in X2GO and if we had all the students use X2GO we would not need to use public IP addresses for each DSVM. But for now, Jupyter is accessible though browser using the https://”FQDN”:8000 and logging into the server with the same username and password. UWStudent UW3tudent

   

  I have not had a chance to look into remote IPython kerneal access yet. I should have some time early next week.

   

  I found the following links helpful:

  This is a basic HowTo DSVM page https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/linux-dsvm-walkthrough

  Here is a link to the X2GO app, the link is also on the MS site. https://wiki.x2go.org/doku.php

   

   

  -Chad

   

   

   

  From: Stephen Elston [mailto:Stephen.Elston@quantia.com]
  Sent: Thursday, February 15, 2018 1:15 PM
  To: Chad Sleeman <sleeman1@uw.edu>
  Cc: Vadim Karpusenko <vadim.karpusenko@microsoft.com>; Piyu Roy <piyuroy@uw.edu>; Rudy Garcia <rudy514@uw.edu>; Brendan Impson <bimpson@uw.edu>; uw_continuum_it_infrastructure <uw_continuum_it_infrastructure@uw.edu>
  Subject: Re: login info for DSVM

   

  Thanks for the follow up Chad.

   

  Also it will be useful if we can run remote IPython kernels. This will allow us to use Spyder or Python IDEs for debugging:  https://github.com/ipython/ipython/wiki/Cookbook:-Connecting-to-a-remote-kernel-via-ssh  If this is too hard we can probability survive without it. 

   

  Hope you actually get some time off on your day off!

   

  Regards, Steve

   

   

   

   

  From: Chad Sleeman <sleeman1@uw.edu>
  Sent: Thursday, February 15, 2018 1:05:34 PM
  To: Stephen Elston
  Cc: Vadim Karpusenko; Piyu Roy; Rudy Garcia; Brendan Impson; uw_continuum_it_infrastructure
  Subject: RE: login info for DSVM

   

  The DevTest labs in Azure run the VM’s on a private subnet and forward ports in.  I am thinking we will need to change this and use a public IP/subnet or each student would need to connect to Jupyter with a different port.

   

  I am going to have to do some research to see if my assumption is correct. I am also going to look at our other DevTest labs for SQL and see if each VM  has a public IP or if they use different ports for each VM. Brendan and John set up the SQL class, they may have ran into this same issue.

   

  Chad

   

  From: Stephen Elston [mailto:Stephen.Elston@quantia.com]
  Sent: Thursday, February 15, 2018 12:25 PM
  To: Chad Sleeman <sleeman1@uw.edu>
  Cc: Vadim Karpusenko <vadim.karpusenko@microsoft.com>; Piyu Roy <piyuroy@uw.edu>; Rudy Garcia <rudy514@uw.edu>; Brendan Impson <bimpson@uw.edu>; uw_continuum_it_infrastructure <uw_continuum_it_infrastructure@uw.edu>
  Subject: Re: login info for DSVM

   

  ps -aux | grep 'anaconda'

  root       1157  0.0  0.5 281384 48096 ?        Ss   18:30   0:03 /anaconda/envs/py35/bin/python /anaconda/envs/py35/bin/jupyterhub --log-file=/var/log/jupyterhub.log

  root       1168  0.0  0.0 146344  1592 ?        S    18:30   0:00 runuser -s /bin/bash nobody -c ulimit -S -c 0 >/dev/null 2>&1 ; /anaconda/envs/py35/bin/jupyter notebook

  nobody     1177  0.0  0.0 113128  1208 ?        Ss   18:30   0:00 bash -c ulimit -S -c 0 >/dev/null 2>&1 ; /anaconda/envs/py35/bin/jupyter notebook

  nobody     1180  0.0  0.7 320884 62664 ?        S    18:30   0:03 /anaconda/envs/py35/bin/python /anaconda/envs/py35/bin/jupyter-notebook

  root      26660  0.0  0.0 112664   980 pts/0    S+   20:00   0:00 grep --color=auto anaconda

   

   

  From: Stephen Elston
  Sent: Thursday, February 15, 2018 12:24:49 PM
  To: Chad Sleeman
  Cc: Vadim Karpusenko; Piyu Roy; Rudy Garcia; Brendan Impson; uw_continuum_it_infrastructure
  Subject: Re: login info for DSVM

   

  That works! Thank you. 

   

  Now I am trying to figure out how to display Jupyter notebooks from a server I start in the VM. Do I need to use an SSH tunnel?  I can see that I started the Jupyter processes:

   

  From: Chad Sleeman <sleeman1@uw.edu>
  Sent: Thursday, February 15, 2018 11:41:33 AM
  To: Stephen Elston
  Cc: Vadim Karpusenko; Piyu Roy; Rudy Garcia; Brendan Impson; uw_continuum_it_infrastructure
  Subject: login info for DSVM

   

  You can log into the VM using root with a PW of: Sp4rkysilver!

   

  Chad

   

  From: Chad Sleeman
  Sent: Monday, February 5, 2018 2:08 PM
  To: Stephen Elston <stephen.elston@quantia.com>
  Cc: Vadim Karpusenko <vadim.karpusenko@microsoft.com>; Piyu Roy <piyuroy@uw.edu>; Rudy Garcia <rudy514@uw.edu>; Brendan Impson <bimpson@uw.edu>; uw_continuum_it_infrastructure <uw_continuum_it_infrastructure@uw.edu>; Marlon Buchanan <mlbu@uw.edu>
  Subject: RE: VM for deep learning

   

  Stephen,

   

  We have a DSVM set up for your testing in Azure. Log into portal.azure.com with your UW NetID address sfelston@uw.edu. In Azure, under All resources,  you should see Deep_Learning listed. I have attached an image to help:

   

  In DevTest labs, under My Virtual machines you should see the VM InstructorTest. From the VM you can see the SSH info to connect. You can log into the VM using root with a PWof Sp4rkysilver!

   

  For the students, we will set up a DSSVM for each student and provide a list of user names and passwords for each VM. For now, this is a good start to give you a chance to take a look at the VM and see if it will work for the class needs.

   

  Looking at the DSVM information It looks like while the VM is built with GPU in mind it also works with just CPU? Here is a link, https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoft-ads.linux-data-science-vm-ubuntu and an image highlighted with what I am seeing.

   

   

  -Chad

   

   

  From: Chad Sleeman
  Sent: Friday, February 2, 2018 11:16 AM
  To: Stephen Elston <stephen.elston@quantia.com>
  Cc: Vadim Karpusenko <vadim.karpusenko@microsoft.com>; Piyu Roy <piyuroy@uw.edu>; Rudy Garcia <rudy514@uw.edu>; Brendan Impson <bimpson@uw.edu>
  Subject: Re: VM for deep learning

   

  Stephen,

  I've been out of the office this week, sorry for the delay.

  We will have a DS VM set up for you Monday.

  Chad

  Get Outlook for Android

   

  From: Stephen Elston

  Sent: Friday, February 2, 9:07 AM

  Subject: VM for deep learning

  To: Chad Sleeman

  Cc: Vadim Karpusenko, Piyu Roy

  Hi Chad,

  I  need to start setting  up and testing out the labs for our upcoming deep learning class. Can a VM with GPU be made available? 

  Thank you and best regards, Steve

  Stephen F. Elston, PhD

  Principal Consultant

  Quantia Analytics, LLC

  +1-206-714-9998

  stephen.elston@quantia.com
  Paul Z. Wu
    
  May 18 (1 day ago)
    
  to IELP, me, Brendan, Cheryl, Rudy, Chad
  Hi Chad,

  Thanks. The login info works.

  It is supposed to have a single-node standalone hadoop cluster on it (https://docs.microsoft.com/en-us/azure/machine-learning/data-science-virtual-machine/overview), but I cannot find it. I can see Spark (SPARK_HOME=/dsvm/tools/spark/spark-2.2.0). It is strange: If it were installed, the hadoop command such as "hdfs" would work. We may need support on this.


   
  Paul Z. Wu
   
  http://www.elookinto.com
  Chad Sleeman <sleeman1@uw.edu>
    
  2:21 PM (23 hours ago)
    
  to Paul, IELP, me, Brendan, Cheryl, Rudy

  Paul, I gave your NetID account permissions to make a support request with Microsoft. If you need help or don’t feel comfortable with making the ticket let me know and I can help out.

   

  Chad

   

  From: Paul Z. Wu <zwu_net@yahoo.com>
  Sent: Friday, May 18, 2018 1:57 PM
  To: IELP Big Data Program <intbgdta@uw.edu>; Paul Tremblay <paulhtremblay@gmail.com>; Brendan Impson <bimpson@uw.edu>; Cheryl L. Wheeler <cherylwh@uw.edu>; Rudy Garcia <rudy514@uw.edu>; Chad Sleeman <sleeman1@uw.edu>
  Subject: Re: FW: login info for DSVM
    
  Click here to Reply, Reply to all, or Forward
  1.82 GB (12%) of 15 GB used
  Manage
  Terms - Privacy
  Last account activity: 13 minutes ago
  Details
    
    

