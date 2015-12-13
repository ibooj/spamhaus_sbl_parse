
# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "binarydata/debian-jessie"
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provision "chef_solo" do |chef|
    chef.add_recipe "apt"
    chef.add_recipe "python3"
    chef.add_recipe "locale"
    chef.add_recipe "requirements"
  end

end