import React, { PureComponent } from "react";
import {BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';

const DataFormater = (number) => {
  if(number > 1000000000000){
    return (number/1000000000000).toString() + 'T';
  }else if(number > 1000000000){
    return (number/1000000000).toString() + 'B';
  }else if(number > 1000000){
    return (number/1000000).toString() + 'M';
  }else if(number > 1000){
    return (number/1000).toString() + 'K';
  }else{
    return number.toString();
  }
}


export default class Barchart extends PureComponent {
  render() {
    const lines = []
    const axes = []
    for (const [index, value] of this.props.ydataKeys.entries()) {
      lines.push(<Bar yAxisId={this.props.axes[index]} key={index} type="monotone"
      dataKey={this.props.ydataKeys[index]} fill={this.props.barColors[index]}
      tick={{fontSize: this.props.fontSize, fill:"#CED8D8"}}/>);
    }
    if(this.props.axes.includes("left")){
      axes.push(<YAxis yAxisId="left"
      label={{ value: this.props.ylabel, angle: -90, position: 'center', fontSize: this.props.yfontSize, fill:"#CED8D8", dx: -1*this.props.ymargin}}
      tick={{fontSize: this.props.fontSize, fill:"#CED8D8"}} tickFormatter={DataFormater}/>);
    }
    if(this.props.axes.includes("right")){
      axes.push(<YAxis yAxisId="right" orientation="right"
      label={{ value: this.props.ylabel, angle: 90, position: 'center', fontSize: this.props.yfontSize, fill:"#CED8D8", dx: 1*this.props.ymargin}}
      tick={{fontSize: this.props.fontSize, fill:"#CED8D8"}} tickFormatter={DataFormater}/>);
    }
    return (
      <div className="noselect">
      <div  className="chartTitle">{this.props.title}</div>
      <BarChart
        width={this.props.width}
        height={this.props.height}
        data={this.props.data}
        margin={{
          top: 10, bottom: this.props.xmargin, right:30,left:this.props.ymargin
        }}
      >
        <CartesianGrid fill={this.props.fill}/>
        <XAxis interval={this.props.interval} label={{value: this.props.xlabel, angle: 0, position: 'center', fontSize: this.props.xfontSize, fill:"#CED8D8", dy: this.props.xmargin}}
        dataKey={this.props.x} tick={{angle:this.props.angle,fontSize: this.props.fontSize, fill:"#CED8D8",dy:this.props.xtmargin,dx:this.props.xshift}}/>
        {axes}
        <Tooltip labelStyle={{fontSize:this.props.tipfontSize}} wrapperStyle={{fontSize: this.props.tipTwofontSize, fill: "#CED8D8"}} formatter={DataFormater} />
        <Legend layout="vertical" verticalAlign="top" align="right" align="right" wrapperStyle={{fontSize: this.props.fontSize, fill:"#CED8D8",paddingLeft: this.props.legendPadding}}/>
        {lines}
      </BarChart>
      </div>
    );
  }
}
