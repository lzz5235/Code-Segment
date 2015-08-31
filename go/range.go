package main

import (
	"fmt"
)

func main() {
	s := []string{"a", "b", "c"}

	for k, v := range s {
		go func(k int, v string) {
			fmt.Printf("k: %d    v:%s\n", k, v)

		}(k, v)
	}
	select {}
}
