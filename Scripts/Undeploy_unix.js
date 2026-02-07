var stopperCommand = [
    "/bin/bash",
    "-c",
    "/home/path/stopper.sh > /home/path/mirth_stopper.log 2>&1"
];

try {
    logger.warn("Executing stopper.sh to terminate background Python processes...");
    
    var processBuilder = new java.lang.ProcessBuilder(stopperCommand);
    
    processBuilder.directory(new java.io.File("/home/path/Scripts"));
    
    var process = processBuilder.start();
    
    var exitCode = process.waitFor();
    
    logger.warn("stopper.sh executed with exit code: " + exitCode + ". Processes should be terminated.");
    
} catch (e) {
    logger.error("FATAL Error executing stopper.sh: " + e.toString());
}
