#!/bin/bash


function restart_server(){
  if [[ ${USER} != "root" ]];then
    sudo init 6
  else:
    init 6
  fi
}

restart_server
