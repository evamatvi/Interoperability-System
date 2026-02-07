function stopProc(key) {
    var p = globalMap.get(key);

    if (p != null) {
        try {
            p.destroy();
            java.lang.Thread.sleep(1500);

            // si encara segueix viu, força
            try { p.destroyForcibly(); } catch (e2) {}

            logger.warn("Stopped process: " + key);
        } catch (e) {
            logger.error("Error stopping " + key + ": " + e);
        } finally {
            globalMap.remove(key);
        }
    } else {
        logger.warn("No process found for key: " + key);
    }
}

stopProc("P_WORKLIST");
stopProc("P_DICOMIZER");
stopProc("P_STORAGE");
