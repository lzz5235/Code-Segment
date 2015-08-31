package main

import (
	"fmt"
	//"runtime"
	"time"
)

var c chan bool

func ready(w string, sec int) {
	time.Sleep(time.Duration(sec) * time.Second)
	fmt.Println(w, "is ready!")
	c <- true
}

func main() {
	c = make(chan bool)
	go ready("Tea", 2)
	go ready("Coffee", 1)

	fmt.Println("I am waiting")
	time.Sleep(3 * time.Second)
	<-c
	<-c
}
