var command = [
    "/bin/bash",
    "-c",
    // Redireccionamiento para loguear errores y salida en segundo plano
    "/home/path/runner.sh > /home/path/mirth_runner.log 2>&1"
];

try {
    // 1. Delay de 5 segundos
    logger.info("Waiting 5 seconds before executing runner.sh...");
    java.lang.Thread.sleep(5000);
    
    var processBuilder = new java.lang.ProcessBuilder(command);
    
    // 2. Directorio de trabajo
    processBuilder.directory(new java.io.File("/home/path/Scripts"));
    
    // 3. INICIAR Y CONTINUAR
    var process = processBuilder.start();
    
    logger.info("runner.sh launched successfully. Processes running in background.");
    
} catch (e) {
    logger.error("FATAL Error executing runner.sh: " + e.toString());
}

