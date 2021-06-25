#!/bin/bash

#action=$1
file_server="xx.xx.xx.xx:xx"
work_dir="/home/xxx/"
shell_dir="/xxx/shell"



function download_tool() {
  if [[  -f ${work_dir}install_tool.tgz  ]];then
    echo "file exist,now remove"
    sudo rm -rf ${work_dir}install_tool.tgz
  elif [[  -d ${work_dir}install_tool ]];then
    sudo rm -rf ${work_dir}install_tool
  fi
  wget -P ${work_dir} http://${file_server}/e99917c6-0829-439d-9f86-45ceb7ca1163/install_tool.tgz
  cd ${work_dir}
  tar zxvf install_tool.tgz
  if [[  -f ${work_dir}install_tool.tgz ]];then
    sudo rm -rf ${work_dir}install_tool.tgz
  fi
}

function execute() {
  cd ${work_dir}install_tool/bin
  echo "start install"
  python3 waf_deploy_tool.py -I $OPTARG
  sleep 5
  echo "haproxy setup"
  python3 waf_deploy_tool.py -C
  sleep 5
  echo "after install setup"
  python3 waf_deploy_tool.py -A
  add_crontab
}

function del_dir() {
  if [[  -d ${work_dir}install_tool  ]];then
    echo "execute done,now remove tempfile"
    sudo rm -rf ${work_dir}install_tool
  fi
}

function add_crontab() {
  cd ${work_dir}install_tool/bin
  echo "add crontab check ha"
  sudo python3 waf_deploy_tool.py -ac
}

function add_reboot_crontab() {
  cd ${work_dir}install_tool/bin
  echo "add crontab check ha"
  sudo python3 waf_deploy_tool.py -S $OPTARG
}

function check_gateway_status() {
  cd ${work_dir}install_tool/bin
  echo "check gateway status"
  python3 waf_deploy_tool -i check_gateway_status
}

function rebootserver() {
  sudo init 6
}

function install() {
  download_tool
  execute
  #echo "install completed ,now will reboot server"
  #sleep 10
  #rebootserver
}

while getopts ":I:rcaS:h" optname
do
    case "$optname" in
      "I")
        install $OPTARG
        del_dir
        ;;
      "r")
        rebootserver
        ;;
      "c")
        download_tool
        check_gateway_status
        del_dir
        ;;
      "a")
        download_tool
        add_crontab
        del_dir
        ;;
      "S")
        download_tool
        add_reboot_crontab $OPTARG
        del_dir
        ;;
      "h")
        echo "get help option -h,eg:./$0 {-I test_waf}"
        ;;
      ":")
        echo "No argument value for option $OPTARG"
        exit 1
        ;;
      "?")
        echo "Unknown option $OPTARG"
        exit 1
        ;;
      *)
        echo "Unknown error while processing options"
        ;;
    esac
done
