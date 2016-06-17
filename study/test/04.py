#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"
import pdb
import sys
month_d=[31,29,31,30,31,30,31,31,30,31,30,31]
month_d_leap=[31,28,31,30,31,30,31,31,30,31,30,31]
def sum_days(list_,month,day):
    days_num=0
    for i in range(1,month):
        days_num+=list_[i]
    days_num+=day
    return days_num


def _is_leap(year):
    mod=year%4
    if mod==0:
        return True
    else:
        return False

def main():
    # year=sys.argv[1]
    # month=sys.argv[2]
    # day=sys.argv[3]
    year=int(raw_input("Pls input Year: \n"))
    month=int(raw_input("Pls input Month: \n"))
    day=int(raw_input("Pls input Day: \n"))
    if _is_leap(year):
        month_day=month_d_leap
    else:
        month_day=month_d
    days_num=sum_days(month_day,month,day)
    output="{year} year\t{month} month\t{day} days\thas {day_num} days!".format(year=year,month=month,day=day,day_num=days_num)
    print output


if __name__ == '__main__':
    main()
