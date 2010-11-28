new Highcharts.Chart({
		chart: {
			renderTo: 'graph',
			defaultSeriesType: 'spline',
			zoomType: 'x'
		},
	        title: {
			text: '{{cur_company.name}}  {{ cur_company.sentiment_count }} Sentiments  ' + Highcharts.numberFormat({{ cur_company.average_value }}, 2) + ' Rating'
		},
	        subtitle: {
			text: 'Click and drag in the plot area to zoom in'
		},
		xAxis: {
			type: 'datetime',
			maxZoom: 3600000, // one hour
			title: {
				text: null
			}
		},
		yAxis: {
			title: {
				text: 'Rating'
			},
			startOnTick: false,
			showFirstLabel: false
		},
		tooltip: {
			formatter: function() {
				return ''+
					'<b>'+ this.series.name +'</b><br/>'+
					Highcharts.dateFormat('%Y-%m-%d %H:%M', this.x) + ':'+
					'Rating = '+ Highcharts.numberFormat(this.y, 2);
			}
		},
		legend: {
			enabled: true
		},
		credits: {
	        enabled: false
	    },
		plotOptions: {
         series: {
            cursor: 'pointer',
            point: {
               events: {
                  click: function() {
                  	$('body').data('point', this);
                  	$('body').data('inlinePopContentId', this.series.name + this.x + Math.floor(Math.random()*1000));
                  	
                  	hs.htmlExpand(null, {
                        pageOrigin: {
                           x: $('body').data('point').pageX, 
                           y: $('body').data('point').pageY
                        },
                        headingText: $('body').data('point').series.name + ' ' + Highcharts.dateFormat('%A, %b %e, %Y', this.x),
                        maincontentText: '<div id=\'' + $('body').data('inlinePopContentId') + '\' class=\'inlinePopContent\'><img class=\'inlinePopLoader\' src=\'/media/images/ajax-loader.gif\'/></div>',
                        width: 500,
                        height: 400
                     });
                    $.ajax({
					      url: 'records',
					      type: 'get',
					      data: ({
					      	key : $('body').data('point').config[2]
					      }),
					      dataType: 'html',
					      success: function(data) {
					      	//console.log($('body').data('point'));
						    $('#' + $('body').data('inlinePopContentId')).html(data);
			  
						  }
					});
                  	

                  }
               }
            }
         }
      },
	  {{ series }}
	});