#include "list.h"
#define MAX_LEN 256

struct task_struct{
	list_head priority_list;
	list_head timer_list;
	int priority;
	int timeout;
	char name[MAX_LEN];
};

struct task_struct* init_task(int priority,int timeout,char *name,int str_len)
{
	struct task_struct *T = (struct task_struct * )malloc(sizeof(struct task_struct));
	T->priority = priority;
	T->timeout = timeout;
	strncpy(T->name,name,str_len);
	return T;

}

struct list_head* p_add_task(list_head *head,struct task_struct *task)
{
	struct list_head *pos;
	struct task_struct *p;
	if(list_empty(head))
	{
		list_add(&task->priority_list,head);
		return head;
	}
	list_for_each(pos,head)//big->little
	{
		p=list_entry(pos, struct task_struct, priority_list);
		if( p->priority  < task->priority)//insert node > current node
		{
			list_add(&task->priority_list,pos->prev);
			return head;
		}
	}
	list_add_tail(&task->priority_list,head);
	return head;
}
struct list_head* t_add_task(list_head *head,struct task_struct *task)
{
	struct list_head *pos;
	struct task_struct *p;
	if(list_empty(head))
	{
		list_add(&task->timer_list,head);
		return head;
	}
	list_for_each(pos,head)//little ->big
	{
		p=list_entry(pos, struct task_struct, timer_list);
		if( p->timeout  > task->timeout)//insert node > current node
		{
			list_add(&task->timer_list,pos->prev);
			return head;
		}
	}
	list_add_tail(&task->timer_list,head);
	return head;
}

struct task_struct* p_del_task(list_head *head,struct task_struct *task)
{
	list_del(&task->priority_list);
	return task;
}
struct task_struct* t_del_task(list_head *head,struct task_struct *task)
{
	list_del(&task->timer_list);
	return task;
}

int Print_priority_list(struct task_struct *task)
{
	struct list_head *pos;
	struct task_struct *p;
	printf("P\tT\tN\n");
	list_for_each(pos,&task->priority_list)
	{
		p=list_entry(pos, struct task_struct, priority_list);
		printf("%d\t%d\t%s\n", p->priority,p->timeout,p->name);
	}
}

int Print_timer_list(struct task_struct *task)
{
	struct list_head *pos;
	struct task_struct *p;
	printf("P\tT\tN\n");
	list_for_each(pos,&task->timer_list)
	{
		p=list_entry(pos, struct task_struct, timer_list);
		printf("%d\t%d\t%s\n", p->priority,p->timeout,p->name);
	}
}

int main()
{
	struct task_struct head={
		.priority_list = LIST_HEAD_INIT(head.priority_list),
		.timer_list = LIST_HEAD_INIT(head.timer_list),
 		.priority = -1,
		.timeout = -1,
		.name = NULL
	};

	char temp1[MAX_LEN] = "T1";
	char temp2[MAX_LEN] = "T2";
	char temp3[MAX_LEN] = "T3";
	struct task_struct *T1,*T2,*T3;
	T1 = init_task(1,10,temp1,strlen(temp1));
	T2 = init_task(3,5,temp2,strlen(temp2));
	T3 = init_task(2,2,temp3,strlen(temp3));
	
	p_add_task(&head.priority_list,T2);
	p_add_task(&head.priority_list,T3);
	p_add_task(&head.priority_list,T1);

	t_add_task(&head.timer_list,T3);
	t_add_task(&head.timer_list,T2);	
	t_add_task(&head.timer_list,T1);
	


	Print_priority_list(&head);
	printf("\n");
	Print_timer_list(&head);

	p_del_task(&head.priority_list,T2);
	p_del_task(&head.priority_list,T3);
	p_del_task(&head.priority_list,T1);

	t_del_task(&head.timer_list,T3);
	t_del_task(&head.timer_list,T2);
	t_del_task(&head.timer_list,T1);
	return 0;
}
