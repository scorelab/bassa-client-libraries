package logger

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
)

// InfoLogger : log general info
var InfoLogger *log.Logger

// ErrorLogger : log errors and exceptions
var ErrorLogger *log.Logger

func init() {
	absPath, err := filepath.Abs("./")
	if err != nil {
		fmt.Println("Error reading given path:", err)
	}

	LogFile, err := os.OpenFile(absPath+"/bassa-log.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println("Error opening file:", err)
		os.Exit(1)
	}
	InfoLogger = log.New(LogFile, "Info Logger:\t", log.Ldate|log.Ltime|log.Lshortfile)
	ErrorLogger = log.New(LogFile, "Error Logger:\t", log.Ldate|log.Ltime|log.Lshortfile)
}
