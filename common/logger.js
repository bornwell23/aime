// Browser-compatible logging utility
class Logger {
  constructor({
    serviceName = 'default', 
    logLevel = process.env.VUE_APP_LOG_LEVEL || 'INFO', 
    logToConsole = true,
    sendRemoteLog = false,
  }) {
    this.serviceName = serviceName;
    this.logLevel = logLevel.toUpperCase();

    // Log levels with numeric priority
    this.LEVELS = {
      ERROR: 0,
      WARN: 1,
      INFO: 2,
      DEBUG: 3
    };

    this.logToConsole = logToConsole;
    this.sendRemoteLog = sendRemoteLog;
  }

  // Internal method to format log message
  _formatMessage(level, message) {
    const timestamp = new Date().toISOString();
    return `${timestamp} [${this.serviceName.toUpperCase()}] ${level}: ${message}`;
  }

  // Internal logging method with level checking
  _log(level, message) {
    // Check if the current log level allows this message
    if (this.LEVELS[level] <= this.LEVELS[this.logLevel]) {
      const formattedMessage = this._formatMessage(level, message);

      // Log to console if enabled
      if (this.logToConsole) {
        switch (level) {
          case 'ERROR':
            console.error(formattedMessage);
            break;
          case 'WARN':
            console.warn(formattedMessage);
            break;
          case 'INFO':
            console.info(formattedMessage);
            break;
          case 'DEBUG':
            console.debug(formattedMessage);
            break;
        }
      }

      // Optional: Send logs to a remote logging service
      if (this.sendRemoteLog) {
        this._sendRemoteLog(level, formattedMessage);
      }
    }
  }

  // Optional method to send logs to a remote service
  _sendRemoteLog(level, message) {
    // Implement remote logging if needed
    // This could be an API call to a logging service
    try {
      // Example placeholder for remote logging
      if (level === 'ERROR' && window.fetch) {
        fetch('/api/logs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            level, 
            message, 
            serviceName: this.serviceName 
          })
        }).catch(console.error);
      }
    } catch (error) {
      // Silently catch any logging errors
      console.error('Remote logging failed:', error);
    }
  }

  // Public logging methods
  error(message) {
    this._log('ERROR', message);
  }

  warn(message) {
    this._log('WARN', message);
  }

  info(message) {
    this._log('INFO', message);
  }

  debug(message) {
    this._log('DEBUG', message);
  }

  // Flexible logging method
  log(level, message) {
    const upperLevel = level.toUpperCase();
    if (!this.LEVELS.hasOwnProperty(upperLevel)) {
      throw new Error(`Invalid log level. Must be one of: ${Object.keys(this.LEVELS).join(', ')}`);
    }
    this._log(upperLevel, message);
  }
}

export { Logger };
