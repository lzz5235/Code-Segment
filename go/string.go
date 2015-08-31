package main

import (
	"fmt"
)

func main() {
	s := "Hello golang"
	c := []rune(s)
	c[0] = 'E'
	fmt.Println(string(c))
}
