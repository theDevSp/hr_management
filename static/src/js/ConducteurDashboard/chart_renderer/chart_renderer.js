/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted, useEffect, onWillUnmount } = owl

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart")

        onWillStart(async () => {
            await loadJS("/configuration_module/static/src/libraries/ChartJS/chart.umd.min.js")
        })


        useEffect(() => {
            this.renderChart()
        }, () => [this.props.config])

        onMounted(() => this.renderChart())

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy()
            }
        })
    }

    renderChart() {

        if (this.chart) {
            this.chart.destroy()
        }

        this.chart = new Chart(this.chartRef.el, {
            type: this.props.type,
            data: this.props.config,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: this.props.title,
                        position: 'bottom',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            },
        });
    }
}

ChartRenderer.template = "owl.ChartRenderer"