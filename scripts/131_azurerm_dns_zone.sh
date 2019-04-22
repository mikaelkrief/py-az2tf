
azr=`az network dns zone list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" != "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        zt=`echo $azr | jq ".[(${i})].zoneType" | tr -d '"'`
        resvn=`echo $azr | jq ".[(${i})].resolutionVirtualNetworks" | tr -d '"'`
        regvn=`echo $azr | jq ".[(${i})].registrationVirtualNetworks" | tr -d '"'`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t zone_type = \"%s\"\n" $zt >> $outfile
        
        
        #
        printf "}\n" >> $outfile
        #
      
    done
fi
