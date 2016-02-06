/**
 * Created by shane on 2016/1/2.
 */
$( document ).ready(function() {
    var gauge1 = loadLiquidFillGauge("fillgauge1", 0);
    var gauge2 = loadLiquidFillGauge("fillgauge2", 0);
    var gauge3 = loadLiquidFillGauge("fillgauge3", 0);
    var gauge4 = loadLiquidFillGauge("fillgauge4", 0);
    var gauge5 = loadLiquidFillGauge("fillgauge5", 0);
    all_team=[];
    for(i=0;i<raw_data.length;i++){
        all_team.push(raw_data[i].home_team);
    }
    all_team=all_team.reverse().filter(function (e, i, arr) {
        return arr.indexOf(e, i+1) === -1;
    }).reverse();
    for(i=0;i<all_team.length;i++){
        $('#team_sel').append('<option>'+all_team[i]+'</option>');
    }
    $('#team_sel').multiselect({
            enableFiltering: true,
            filterPlaceholder: 'Search for team',
            buttonWidth: '200px',
            onChange: function(option, checked) {
                //alert($('#team_sel').val());
                filter_data = raw_data.filter(function (el) {
                                return el.home_team == $('#team_sel').val() || el.away_team == $('#team_sel').val()
                            }).map(function(x){
                                return x.over_under_result
                            });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);


                gauge1.update(num)
                console.log(filter_data)
            }
        });
    $("#locations_sel").bootstrapSwitch({
            onText: 'Home',
            offText: 'Away',
            size: 'small',
            labelText: 'Location',
            offColor: 'info'
    });
    $('#locations_sel').on('switchChange.bootstrapSwitch', function (event, state) {
        if(state){
            console.log('Home');
                filter_data = raw_data.filter(function (el) {
                                return el.home_team == $('#team_sel').val()
                            }).map(function(x){
                                return x.over_under_result
                            });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
            gauge2.update(num)
        }
        else{
            console.log('Away');
                filter_data = raw_data.filter(function (el) {
                                return el.away_team == $('#team_sel').val()
                            }).map(function(x){
                                return x.over_under_result
                            });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
            gauge2.update(num)
        }
    });
    $("#conferences_sel").bootstrapSwitch({
            onText: 'East',
            offText: 'West',
            size: 'small',
            labelText: 'Conference',
            offColor: 'info'
    });
    $('#conferences_sel').on('switchChange.bootstrapSwitch', function (event, state) {
        if(state){
            console.log('East')
            filter_data = raw_data.filter(function (el) {
                                return (el.home_team == $('#team_sel').val() && el.away_conf == 'E')
                                    || (el.away_team == $('#team_sel').val() && el.home_conf == 'E')
                            }).map(function(x){
                                return x.over_under_result
                        });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
            gauge3.update(num)
        }
        else{
            console.log('West')
            filter_data = raw_data.filter(function (el) {
                                return (el.home_team == $('#team_sel').val() && el.away_conf == 'W')
                                    || (el.away_team == $('#team_sel').val() && el.home_conf == 'W')
                            }).map(function(x){
                                return x.over_under_result
                        });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
            gauge3.update(num)
        }
    });
    $("#conferences_sel").bootstrapSwitch({
            onText: 'East',
            offText: 'West',
            size: 'small',
            labelText: 'Conference',
            offColor: 'info'
    });
    $("#winning_percentage_sel").bootstrapSwitch({
            onText: '>=50%',
            offText: '<50%',
            size: 'small',
            labelText: 'Winning Percentage',
            offColor: 'info'
    });
    $('#winning_percentage_sel').on('switchChange.bootstrapSwitch', function (event, state) {
        if(state){
            console.log('>=50%')
            filter_data = raw_data.filter(function (el) {
                                return (el.home_team == $('#team_sel').val() && el.away_winning_percent >= 0.5)
                                    || (el.away_team == $('#team_sel').val() && el.home_winning_percent >= 0.5)
                            }).map(function(x){
                                return x.over_under_result
                        });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
            gauge4.update(num)
        }
        else{
            console.log('<50%')
            filter_data = raw_data.filter(function (el) {
                                return (el.home_team == $('#team_sel').val() && el.away_winning_percent < 0.5)
                                    || (el.away_team == $('#team_sel').val() && el.home_winning_percent < 0.5)
                            }).map(function(x){
                                return x.over_under_result
                        });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
            gauge4.update(num)
        }
    });
    $('#weekday_sel').multiselect({
            buttonWidth: '200px',
            onChange: function(option, checked) {
                //alert($('#weekday_sel').val());
                filter_data = raw_data.filter(function (el) {
                                return (el.home_team == $('#team_sel').val() && el.weekday == $('#weekday_sel').val())
                                    || (el.away_team == $('#team_sel').val() && el.weekday == $('#weekday_sel').val())
                            }).map(function(x){
                                return x.over_under_result
                        });
                num = (100*filter_data.filter(function (el) {
                                return el == 'over'
                            }).length/filter_data.length).toFixed(0);
                console.log(filter_data)
                gauge5.update(num)
            }
    });


});

