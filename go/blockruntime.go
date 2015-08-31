package main

import (
	"fmt"
	//	"runtime"
)

func main() {
	ch := make(chan int)
	quit := make(chan bool)

	go show(ch, quit)
	for i := 0; i < 10; i++ {
		ch <- i
	}

	quit <- false
}

func show(c chan int, quit chan bool) {
	for {
		select {
		case j := <-c:
			fmt.Println(j)
			break
		case _ = <-quit:
			break
		}
	}
}
