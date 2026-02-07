var PYTHON = "C:/Users/path/python.exe";
var SCRIPTS_DIR = "C:/Users/path/Scripts";

function jstr(x) {
    return new java.lang.String(String(x));
}

function startProc(key, scriptName, logName) {
    var scriptPath = SCRIPTS_DIR + "/" + scriptName;
    var logPath = SCRIPTS_DIR + "/" + logName;

    // IMPORTANT: tot convertit a java.lang.String
    var cmd = java.util.Arrays.asList([
        jstr("cmd.exe"),
        jstr("/C"),
        jstr("\"" + PYTHON + "\" \"" + scriptPath + "\" > \"" + logPath + "\" 2>&1")
    ]);

    var pb = new java.lang.ProcessBuilder(cmd);
    pb.directory(new java.io.File(SCRIPTS_DIR));
    pb.redirectErrorStream(true);

    var p = pb.start();

    globalMap.put(key, p);
    logger.info("Started " + scriptName + " | log=" + logPath);
}

startProc("P_WORKLIST", "worklist.py", "worklist.log");
startProc("P_DICOMIZER", "dicomitzador.py", "dicomitzador.log");
startProc("P_STORAGE", "storage.py", "storage.log");
