#!/bin/bash
EXTERNAL_API_CIDR=$1
OTHERS_VPC_CIDRS_BLOCKS=$2
LOCAL_IP_NAT=$3
LOAD_BALANCER_DNS=$4

# Get existing iptables rules destination ip and the ones that report the load balancer dns and compare them
IP_ALB_OLD=($(iptables --list PREROUTING -n -t nat | grep DNAT | sed -e 's#.*to:\(\)#\1#' | sed -e 's/:443//g' | sort | uniq))
INTERNAL_LOAD_BALANCER_IPS=($(dig $4 +short | grep -v amazonaws.com))
DIFF=(`echo ${IP_ALB_OLD[@]} ${INTERNAL_LOAD_BALANCER_IPS[@]} | tr ' ' '\n' | sort | uniq -u `)

if [ ${#DIFF} -gt 0 ];
then
  echo "${INTERNAL_LOAD_BALANCER_IPS[@]}"
  INTERNAL_LOAD_BALANCER_IPS_MAX_ITERATIONS=$(( ${#INTERNAL_LOAD_BALANCER_IPS[*]} - 1 ))
  iptables -F PREROUTING -t nat
  for i in $(seq 0 $INTERNAL_LOAD_BALANCER_IPS_MAX_ITERATIONS); do
    if [ ! $i -eq $INTERNAL_LOAD_BALANCER_IPS_MAX_ITERATIONS ];
    then
      IPTABLES_STATISTIC_MODULE="-m state --state NEW -m statistic --mode random --probability .5"
    fi

    iptables -t nat -A PREROUTING -s $EXTERNAL_API_CIDR -p tcp --dport 443 $IPTABLES_STATISTIC_MODULE -j DNAT --to-destination ${INTERNAL_LOAD_BALANCER_IPS[$i]}:443
    #rule to permit traffic from clave VPN
    iptables -t nat -A PREROUTING -s $OTHERS_VPC_CIDRS_BLOCKS -d $LOCAL_IP_NAT -p tcp --dport 443 $IPTABLES_STATISTIC_MODULE -j DNAT --to-destination ${INTERNAL_LOAD_BALANCER_IPS[$i]}:443
    unset IPTABLES_STATISTIC_MODULE
    netfilter-persistent save && netfilter-persistent reload
  done
else
  echo "No hay differencias"
fi