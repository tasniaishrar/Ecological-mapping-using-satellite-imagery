import { Component, EventEmitter, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import Map from 'ol/Map';
import View from 'ol/View';
import VectorLayer from 'ol/layer/Vector';
import Style from 'ol/style/Style';
import Icon from 'ol/style/Icon';
import OSM from 'ol/source/OSM';
import * as olProj from 'ol/proj';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';
import { fromLonLat } from 'ol/proj';
import ZoomSlider from 'ol/control/ZoomSlider.js';
import {Feature, Overlay} from 'ol/index.js';
import { Vector as VectorSource} from 'ol/source.js';
import {Point} from 'ol/geom.js';
import {useGeographic} from 'ol/proj.js';
import {defaults as defaultControls} from 'ol/control.js';
import { RESTAPIServiceService } from '../restapiservice.service';
import {toStringHDMS} from 'ol/coordinate';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit, OnChanges {

  @Output() disp = new EventEmitter<string>();

  // Basic reqs for displaying map
  planetApiKey = "87fe6eed3b5a41b0a37e73da65eb687f"
  emap: any

  // To add time slider
  year= "2023"
  month = "01"
  
  received: boolean = false
  // To keep constant coordinates
  place:any = [-122.395, 37.783]
  // point = new Point(this.place)

  view: any
  data: any
  cordX=0.0
  cordY=0.0
  check: any

  disasters_dict: {[key: string]: number[]}= {
    "socal": [-116,33], //nodecimal
    "santa": [ -122.731547,38.469140],  // ends 0
    "palu" : [119.889349,-0.834806],
    "midwest" : [-90.670364,46.187150], // ends 0
    "mex" : [-101.445760, 18.874770], //ends 0
    "michael" : [-80.860251, 28.034882],
    "mathew" : [-73.158462, 19.810257],
    "harvey" : [-92.314043, 29.912784],
    "florence" : [-76.997224,34.925975],
    "guatamela" : [-90.880957, 14.474586]
  }

  constructor(private __apiservice: RESTAPIServiceService, private cdr: ChangeDetectorRef) { }
  ngOnChanges(): void {
    this.updateCenter()
  }


  onClickMe(g: any) {
      this.__apiservice.getImages(this.cordY, this.cordX).subscribe((res: any) => {
        this.data = res
        this.received = true
        console.log(this.data)
        this.cdr.detectChanges();
        this.disp.emit(this.data);
      })
  }

  updateCenter() {
    //Updates the info of lat and lon
    this.emap.on('moveend', ()=> {
      // this.place = olProj.transform(this.emap.getView().getCenter(), 'EPSG:3857', 'EPSG:4326')
      this.place = this.emap.getView().getCenter()
    });
  }


  ngOnInit(){
    this.received = false
    useGeographic();
    this.emap = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          preload: Infinity,
          source: new XYZ({
            url: 'https://tiles{0-3}.planet.com/basemaps/v1/planet-tiles/global_monthly_2020_01_mosaic/gmap/{z}/{x}/{y}.png?api_key=' + this.planetApiKey
          })
        })
      ],
      view: new View({
        center: [-122.395, 37.783],
        zoom: 12
      })
    })
  }  

  setView(event: any) {
    var target = event.target || event.srcElement || event.currentTarget
    var id = target.getAttribute('id')
    if (id in this.disasters_dict) {
      this.place = this.disasters_dict[id]
      this.emap.getView().setCenter(this.disasters_dict[id])
      this.cordX = this.disasters_dict[id][0]
      this.cordY = this.disasters_dict[id][1]
    }
    
  }

}
