module lingyu.chuanqi {
                /*-*begin $area1*-*/
//这里填写类上方的手写内容
/*-*end $area1*-*/
                /**
                 * 由lingyuH5数据生成工具，从D:\design\传奇配置\DesignData\充值奖励\ShouChong.xlsx生成
                 * 创建时间：2017-10-12 10:38:47
                 **/
                export class ShouChongCfg {
            /**
            * 编号
            **/
            public id: string;
            /**
            * 道具
            **/
            public daoju: string;
            /**
            * 定制装备
            **/
            public zhuangbei: string;
            /**
            * 职业
            **/
            public job: string;
            
            /*-*begin $area2*-*/
//这里填写类里面的手写内容

        public getCustomized() {
            let arr = [];
            this.zhuangbei.split(";").forEach(str => {
                arr.push(str.split(":")[1]);
            })
            return arr;
        }
/*-*end $area2*-*/
                    public decode(data:any[]){
            			let i = 0;
            
            			this.id = data[i++];
            			this.daoju = data[i++];
            			this.zhuangbei = data[i++];
            			this.job = data[i++];
            
            /*-*begin $decode*-*/
//这里填写方法中的手写内容
/*-*end $decode*-*/
                    }
                }
                /*-*begin $area3*-*/
//这里填写类下发的手写内容
/*-*end $area3*-*/
            }