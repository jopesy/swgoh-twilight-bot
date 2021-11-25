# swgoh.help.python
Python code for the API at https://api.swgoh.help/
Api is developed pretty fast so follow it's documentation for changes, I would be able to update this code only irregularly.

## Usage

          creds = settings('your_username','your_password','123','abc')
          client = SWGOHhelp(creds)

#careful, allycode is integer, not string
          
          allycode = 997393984

          player = client.get_data('player',allycode)
          print(player)

          guild = client.get_data('guild',allycode)
          print(guild)

          units = client.get_data('units',allycode)
          print(units)

          battles = client.get_data('battles',allycode)
          print(battles)

#data is different - there the second value is not allycode but chosen collection name:
          
          data = client.get_data('data','abilityList')
          print(data)

#currently valid collections:
          
          abilityList
          battleEnvironmentsList
          battleTargetingRuleList
          categoryList
          challengeList
          challengeStyleList
          effectList
          environmentCollectionList
          equipmentList
          eventSamplingList
          guildExchangeItemList
          guildRaidList
          helpEntryList
          materialList
          playerTitleList
          powerUpBundleList
          raidConfigList
          recipeList
          requirementList
          skillList
          starterGuildList
          statModList
          statModSetList
          statProgressionList
          tableList
          targetingSetList
          territoryBattleDefinitionList
          territoryWarDefinitionList
          unitsList
          unlockAnnouncementDefinitionList
          warDefinitionList
          xpTableList

# Available Language Clients

* JavaScript: https://github.com/r3volved/api-swgoh-help
* Java: https://github.com/j0rdanit0/api-swgoh-help
