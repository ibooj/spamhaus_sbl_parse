#
# Cookbook Name:: python3
# Recipe:: default
#

package "python3"
package "python3-dev"
package "python3-setuptools"
execute "easy_install3 pip"
package "tor"
execute "libxml2-dev"
execute "libxslt1-dev"
