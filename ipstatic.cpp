//海量数据算法:超过10G的日志记录了登录的IP，找出登录次数最多的一个IP

#include <assert.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdint.h>

static_assert(sizeof(void*) == 8, "64-bit only.");

std::vector<uint8_t> counts_;
struct IPcount
{
  uint32_t ip;
  uint32_t count;
  bool operator<(IPcount rhs) const
  { return ip < rhs.ip; }
};
std::vector<IPcount> overflows_;

IPcount top;

void addOverflow(uint32_t ip)
{
  IPcount newItem = { ip, 256 };
  auto it = std::lower_bound(overflows_.begin(), overflows_.end(), newItem);
  if (it != overflows_.end() && it->ip == ip)
  {
    it->count++;
    assert(it->count != 0 && "you need larger count variable");
    newItem.count = it->count;
  }
  else
  {
    overflows_.insert(it, newItem);
  }
  if (newItem.count > top.count)
    top = newItem;
}

void add(uint32_t ip)
{
  if (counts_[ip] == 255)
  {
    addOverflow(ip);
  }
  else
  {
    counts_[ip]++;
    if (counts_[ip] > top.count)
    {
      top.ip = ip;
      top.count = counts_[ip];
    }
  }
}

uint32_t getMostFrequenntIP()
{
  return top.ip;
}

int main()
{
  assert(counts_.max_size() > 0xFFFFFFFFUL);
  counts_.resize(1L << 32);
  printf("%zd\n", counts_.size());

  add(0x1);
  add(0x2);
  add(0x2);
  for (size_t i = 0; i < (1L << 32)-1; ++i)
    add(0x3);
  printf("%08x %u\n", top.ip, top.count);
}
