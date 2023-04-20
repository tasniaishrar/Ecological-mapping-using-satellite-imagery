import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-disp',
  templateUrl: './disp.component.html',
  styleUrls: ['./disp.component.css']
})
export class DispComponent implements OnInit{

  // @Input() RSCDimages: any
  // @Input() gpt_text: any
  // @Input() gpt_text2: any
  // @Input() MLimages: any
  // @Input() original: any
  // @Input() from: any

  @Input() up: any
  @Input() temp: any


  og: boolean = true
  ml: boolean =false
  rs: boolean = false
  gpt: boolean = false



  bare: boolean= true
  build: boolean = false
  grass:boolean=false
  pave:boolean=false
  road:boolean=false
  tree:boolean=false
  water:boolean=false
  crop:boolean=false


  showOG() {
    this.og = true
    this.ml = false
    this.rs = false
    this.gpt = false
  }

  showML() {
    this.og = false
    this.ml = true
    this.rs = false
    this.gpt = false
  }

  showRSCD() {
    this.og = false
    this.ml = false
    this.rs = true
    this.gpt = false
  }

  showGPT() {
    this.og = false
    this.ml = false
    this.rs = false
    this.gpt = true
  }

  rscdImage(img: any) {
    if (img=="Bareland") {
      this.bare= true
      this.build = false
      this.grass=false
      this.pave=false
      this.road=false
      this.tree=false
      this.water=false
      this.crop=false
    }
    if (img=="Buildings") {
      this.bare= false
      this.build = true
      this.grass=false
      this.pave=false
      this.road=false
      this.tree=false
      this.water=false
      this.crop=false      
    }
    if (img=="Grass") {
      this.bare= false
      this.build = false
      this.grass=true
      this.pave=false
      this.road=false
      this.tree=false
      this.water=false
      this.crop=false
    }
    if (img=="Pavemnet") {
      this.bare= false
      this.build = false
      this.grass=false
      this.pave=true
      this.road=false
      this.tree=false
      this.water=false
      this.crop=false
    }
    if (img=="Road") {
      this.bare= false
      this.build = false
      this.grass=false
      this.pave=false
      this.road=true
      this.tree=false
      this.water=false
      this.crop=false
    }
    if (img=="Tree") {
      this.bare= false
      this.build = false
      this.grass=false
      this.pave=false
      this.road=false
      this.tree=true
      this.water=false
      this.crop=false
    }
    if (img=="Water") {
      this.bare= false
      this.build = false
      this.grass=false
      this.pave=false
      this.road=false
      this.tree=false
      this.water=true
      this.crop=false
    }
    if (img=="Cropland") {
      this.bare= false
      this.build = false
      this.grass=false
      this.pave=false
      this.road=false
      this.tree=false
      this.water=false
      this.crop=true
    }
  }

  pp: boolean = true
  rec: boolean=false
  agri:boolean=false
  dis:boolean=false
  con:boolean=false
  urb:boolean=false


  gpt_res(ev:any) {
    if (ev == "gpt_pre_post") {
        this.pp = true
        this.rec=false
        this.agri=false
        this.dis=false
        this.con=false
        this.urb=false
    }
    if (ev == "gpt_rec") {
      this.pp = false
      this.rec=true
      this.agri=false
      this.dis=false
      this.con=false
      this.urb=false
  }
  if (ev == "gpt_agri") {
    this.pp = false
    this.rec=false
    this.agri=true
    this.dis=false
    this.con=false
    this.urb=false
}
if (ev == "gpt_dis") {
  this.pp = false
  this.rec=false
  this.agri=false
  this.dis=true
  this.con=false
  this.urb=false
}
if (ev == "gpt_con") {
  this.pp = false
  this.rec=false
  this.agri=false
  this.dis=false
  this.con=true
  this.urb=false
}
if (ev == "gpt_urb") {
  this.pp = false
  this.rec=false
  this.agri=false
  this.dis=false
  this.con=false
  this.urb=true
}
  }



  ngOnInit() {
    // if (this.from == "upload") {
    //   this.map = false
    // }
    console.log("wjbkubd")
    console.log(this.temp)
  }

}
