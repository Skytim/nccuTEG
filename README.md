安裝nccuTEG
===================================

nccuTEG是基於pybossa所建立的專案,目的在於幫助TEG(電子治理研究中心)分析政府想關的資料  
    以下的教學將透過Vagrant去建立環境
      它是一個輕量級的套件,可以讓你透過virtualbox快速部署專案內定設計的環境


##需求環境
  作業系統
  
1.  ubuntu 14.04LTS
2.  Mac OSX Yosemite

並安裝git

如果是Ubuntu請在termainl輸入

  `apt-get install git`

如果是Mac請下載git安裝
http://sourceforge.net/projects/git-osx-installer/

##設置PyBossa使用Vagrant
你需要安裝以下套件

1.  VirtualBox (min version 4.2.10)
2.  Vagrant (min version 1.2.1)
3.  Vagrant Plugin (vagrant-ansible-local)

安裝完1.2以後安裝3請在終端機輸入:

  `vagrant plugin install vagrant-ansible-local`

之後clone nccuTEG

  `git clone https://github.com/Skytim/nccuTEG`

clone完後,切換到此目錄

  `cd nccuTEG`

並且在terminal輸入指令

  `vagrant up`
  
須等數十分鐘,讓vagrant下載Ubuntu作業系統環境
完成後
進入到虛擬機環境

  `vagrant ssh`
並且運行

  `python run.py`

你現在可以開啟browser並輸入

  `http://127.0.0.1:5000`
  
就可以看到nccuTEG的起始畫面

