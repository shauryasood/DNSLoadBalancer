1)To implement the functionality of the ls server, we used the linux blocking functionality of select(). Because we only needed to read from the ts servers
we used only the first and fourth fields of select.select(), where the first field was a list made up of the sockets of the two ts servers and the forth field
which is a field used to implement a timeout. We set the timeout condition for 5 seconds, so if there is no return string from either ts server then the ls
server will return the error string using a check if-statement to confirm that the readable list is empty.

2)I dont believe any issues are present in our code, there is the concern that creating a new socket each run in the client may make the program vulnerable to
failure as it has to connect to the same port each time multiple times.

3)Problems developing this code was down to understanding how the select() command worked and how/where to implement it in the code. There were also connection
issues between client and servers. It was difficult to troubleshoot as each program either worked or did not with little middle ground, so working in steps was the 
only way.

4)We learned from project 2 how to have multiple connections to a server and how to implement a multifunctional server without using threads.