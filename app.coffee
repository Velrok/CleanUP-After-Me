express = require('express')
exec = require('child_process').exec

# exports.run = ()->
# 	server = express()
# 	server.get '/', (req, res)->
# 		console.log "root called"
# 		res.send("hello world")

# 	server.listen(3000)

# 	console.log "I'm running"

exports.run = ()->
	bla = "blubber"
	exec 'df -h . | grep "/dev/*"', (err, stdout, stderr)->
		if not err
			m = stdout.match(/\d+\w+/g)

			free = m[2]
			free_digits = free[0...free.length-1]
			free_unit = free[free.length-1]

			console.log bla
			console.log "#{free_digits} #{free_unit}"
			# console.log "free -> #{free_bytes}KB  #{free_bytes/1024}MB #{free_bytes/1024/100}GB"