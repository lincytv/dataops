**Production:**

| Probe Host                                                                               | Probe Name            | PA Name     |
|------------------------------------------------------------------------------------------|-----------------------|-------------|
| {{site.data[site.target].oss-sosat.servers.prod.messagebus.us-south.primary.short-name}} | sosat-p-message-bus-1 | DAL_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.prod.messagebus.us-south.backup.short-name}}  | sosat-p-message-bus-2 | DAL_GW02_PA |
| {{site.data[site.target].oss-sosat.servers.prod.messagebus.us-east.primary.short-name}}  | sosat-p-message-bus-1 | WDC_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.prod.messagebus.us-east.backup.short-name}}   | sosat-p-message-bus-2 | WDC_GW02_PA |
| {{site.data[site.target].oss-sosat.servers.prod.messagebus.eu-de.primary.short-name}}    | sosat-p-message-bus-1 | LON_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.prod.messagebus.eu-de.backup.short-name}}     | sosat-p-message-bus-2 | LON_GW02_PA |

**Staging:**

| Probe Host                                                                                | Probe Name            | PA Name     |
|-------------------------------------------------------------------------------------------|-----------------------|-------------|
| {{site.data[site.target].oss-sosat.servers.stage.messagebus.us-south.primary.short-name}} | sosat-p-message-bus-1 | DAL_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.stage.messagebus.us-south.backup.short-name}}  | sosat-p-message-bus-2 | DAL_GW02_PA |
| {{site.data[site.target].oss-sosat.servers.stage.messagebus.us-east.primary.short-name}}  | sosat-p-message-bus-1 | WDC_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.stage.messagebus.us-east.backup.short-name}}   | sosat-p-message-bus-2 | WDC_GW02_PA |
| {{site.data[site.target].oss-sosat.servers.stage.messagebus.eu-de.primary.short-name}}    | sosat-p-message-bus-1 | LON_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.stage.messagebus.eu-de.backup.short-name}}     | sosat-p-message-bus-2 | LON_GW02_PA |

**Dev:**

| Probe Host                                                                      | Probe Name            | PA Name     |
|---------------------------------------------------------------------------------|-----------------------|-------------|
| {{site.data[site.target].oss-sosat.servers.dev.messagebus.us-south.short-name}} | sosat-p-message-bus-1 | DAL_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.dev.messagebus.us-south.short-name}} | sosat-p-message-bus-2 | DAL_GW02_PA |
| {{site.data[site.target].oss-sosat.servers.dev.messagebus.us-east.short-name}}  | sosat-p-message-bus-1 | WDC_GW01_PA |
| {{site.data[site.target].oss-sosat.servers.dev.messagebus.us-east.short-name}}  | sosat-p-message-bus-2 | WDC_GW02_PA |
