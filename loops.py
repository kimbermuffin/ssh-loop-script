#!/usr/bin/env python

import sys
import select
import paramiko

hosts = ['192.168.7.10','192.168.51.10','192.168.52.10','192.168.53.10']

# Connect to the hosts.
for host in hosts:
	print "Attempting communication with %s" % host
	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, username='admin')
		print "Connected to %s" % host
		stdin, stdout, stderr = ssh.exec_command("ver")

		while not stdout.channel.exit_status_ready():
			# Only print data if there is data to read in the channel
			if stdout.channel.recv_ready():
				rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
				if len(rl) > 0:
					# Print data from stdout
					print stdout.channel.recv(1024),

		stdin, stdout, stderr = ssh.exec_command("uptime")

		# Wait for the command to terminate
		while not stdout.channel.exit_status_ready():
			# Only print data if there is data to read in the channel
			if stdout.channel.recv_ready():
				rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
				if len(rl) > 0:
					# Print data from stdout
					print stdout.channel.recv(1024),

		# Disconnect from the host
		print "Command done, closing SSH connection"
		ssh.close()
		#break

	except paramiko.AuthenticationException:
		print "Authentication failed when connecting to %s" % host
		sys.exit(1)
	except:
		print "Could not SSH to %s, try again later." % host
		sys.exit(1)
