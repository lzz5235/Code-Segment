/*题目描述：

“看下面这个图片”

             _ _ 
            |7 7|_
   _        |    6|
  |5|      _|     |
  | |    _|4      |
 _| |  _|3        |
|2  |_|2          | 
|____1____________|
 0 1 2 3 4 5 6 7 8
“在这个图片里我们有不同高度的墙。这个图片由一个整数数组所代表，数组中每个数是墙的高度。上边的图可以表示为数组[2,5,1,2,3,4,7,7,6]”

“假如开始下雨了，那么墙之间的水坑能够装多少水呢？”

             _ _ 
            |7 7|_
   _        |    6|
  |5|█ █ █ █|     |
  | |█ █ █|4      |
 _| |█ █|3        |
|2  |█|2          | 
|____1____________|
 0 1 2 3 4 5 6 7 8
“以1×1的方块为单位计算容积。所以，在上边的图中下标为1以左的都会漏掉。下标7以右的也会漏掉。剩下的只有在1和6之间的一坑水，容积是10”

算法：

读取数据

找出极大值点（包括对头尾两个数据的判断，要决定是否将其放入极大值点中）

递归 寻找极大值数列中高度最高的和第二高的墙。则只要这两堵墙之间的墙的高度n小于他们的最小值m，就可以存储m-n的水。然后分别计算这两堵墙两边的储水情况。*/
#include<stdio.h>
#include<stdlib.h>

int main(void){
        int N;
        int i, j;
        int lefth, righth;
        do{
                scanf("%d", &N);
                if (N <= 0)break;
                int* height = (int *) malloc(sizeof(int) *N);
                for (i = 0; i < N; i++)
                        scanf("%d", &height[i]);
                max_l = height[0];
                max_r = height[N - 1];
                int total = 0;
                i = 0;
                j = N - 1;
                while(i<j)
				{
					if (max_l <= max_r)
					{
						i++;
						if(height[i]>=max_l)
							max_l = height[i];
						else
							total +=(max_l - height[i]);
					}						
					else
					{
						j--;
						if(height[i]>=max_r)
							max_r = height[i];
						else
							total +=(max_r - height[i]);
					}
                }
                printf("totle volume %d\n", total);
        } while (true);
        
        return 0;
}