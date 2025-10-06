import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apt_packages.servergroups import ServerGroups

def setup(bot):
    bot.add_cog(ServerGroups(bot))