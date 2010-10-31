new Highcharts.Chart({
		chart: {
			renderTo: 'graph',
			zoomType: 'x'
		},
	        title: {
			text: '{{cur_company.name}} - {{ cur_company.sentiment_count }} Sentiments - {{ cur_company.average_value }} Rating'
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
			area: {
				fillColor: {
					linearGradient: [0, 0, 0, 300],
					stops: [
						[0, '#4572A7'],
						[1, 'rgba(2,0,0,0)']
					]
				},
				lineWidth: 1,
				marker: {
					enabled: false,
					states: {
						hover: {
							enabled: true,
							radius: 5
						}
					}
				},
				shadow: false,
				states: {
					hover: {
						lineWidth: 1						
					}
				}
			}
		},
		{{ series }}
	});