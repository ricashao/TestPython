<?php
// +----------------------------------------------------------------------
// | ThinkCMF [ WE CAN DO IT MORE SIMPLE ]
// +----------------------------------------------------------------------
// | Copyright (c) 2013-2019 http://www.thinkcmf.com All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: FusionSDK Team <kevin@fusionsdk.com>
// +----------------------------------------------------------------------

namespace app\realname\controller;

use cmf\controller\HomeBaseController;
use app\realname\model\GameAppModel;
use app\realname\model\GameUserModel;
use util\IDCardMgr;
use util\FatigueMgr;
use think\Db;
use think\facade\Cache;

class BindprofileController extends HomeBaseController
{
    public function index()
    {
        $app_id = $this->request->param("appId", 0, 'intval');
        $app = GameAppModel::get($app_id);
        if (!$app) {
            $this->error("该应用不存在");
        }
        $uid = $this->request->param("uid");
        if (!$uid) {
            $this->error("uid参数不能为空");
        }
        $session_id = $this->request->param("sessionId");
        if (!$session_id) {
            $this->error("sessionId参数不能为空");
        }
        $device_id = $this->request->param("deviceId");
        if (!$device_id) {
            $this->error("deviceId参数不能为空");
        }
        $screen = $this->request->param("screen");
        // 应用的实名认证状态禁用时
        if ($app->realname_status == 0) {
            return $this->redirect('Bindprofile/directReturn', [
                'appId' => $app_id,
                'uid' => $uid,
                'sessionId' => $session_id,
                'deviceId' => $device_id
            ]);
        }
        $user = GameUserModel::get([
            'app_id' => $app_id,
            'uid' => $uid,
            'user_type' => 1
        ]);
        if (!$user) {
            $this->assign("app", $app);
            // 窗口模式
            if (!$screen) { // 全屏
                return $this->fetch();
            } else {
                if ($screen == 'mini') {
                    return $this->fetch('index_mini');
                }
                return $this->fetch();
            }
        } else {
            return $this->redirect('Bindprofile/directReturn', [
                'appId' => $app_id,
                'uid' => $uid,
                'sessionId' => $session_id,
                'deviceId' => $device_id
            ]);
        }
    }

    public function profilePost()
    {
        if ($this->request->isPost())
        {
            $req = $this->request->param();
            $uid = $req['uid'];
            $app_id = $req['appId'];
            $session_id = $req['sessionId'];
            $device_id = $req['deviceId'];
            $real_name = $req['real_name'];
            $idcard = $req['idcard'];
            if (!$app_id) {
                $this->error("appId参数<br />不能为空");
            }
            if (!$uid) {
                $this->error("uid参数<br />不能为空");
            }
            if (!$session_id) {
                $this->error("sessionId参数<br />不能为空");
            }
            if (!$device_id) {
                $this->error("deviceId参数<br />不能为空");
            }
            if (!$real_name) {
                $this->error("真实姓名<br />不能为空");
            }
            if (!$idcard) {
                $this->error("身份证号<br />不能为空");
            }
            $manager = new IDCardMgr();
            if (!$manager->valid($idcard))
            {
                $this->error("身份证号<br />无效");
            }
            //走云市场认证
            $host = "https://eid.shumaidata.com";
            $path = "/eid/check";
            $method = "POST";
            $appcode = "d2be366fee9441acbf4e7c863e4a7011";
            $headers = array();
            array_push($headers, "Authorization:APPCODE " . $appcode);
            $querys = "idcard=".$idcard."&name=".urlencode($real_name);
            $bodys = "";
            $url = $host . $path . "?" . $querys;


            $curl = curl_init();
            curl_setopt($curl, CURLOPT_CUSTOMREQUEST, $method);
            curl_setopt($curl, CURLOPT_URL, $url);
            curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
            curl_setopt($curl, CURLOPT_FAILONERROR, false);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            //设定返回信息中是否包含响应信息头，启用时会将头文件的信息作为数据流输出，true 表示输出信息头, false表示不输出信息头
            //如果需要将字符串转成json，请将 CURLOPT_HEADER 设置成 false
            curl_setopt($curl, CURLOPT_HEADER, false);
            if (1 == strpos("$".$host, "https://"))
            {
                curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
                curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
            }
            $res = json_decode(curl_exec($curl));

               
            if($res->code !=0 )
            {
                $this->error($res->message);
            }else{
				if($res->result->res != 1){
					 $this->error("身份证".$res->result->description);
				}
			}

            // 启动事务
            Db::startTrans();
            try {
                // 用户表
                $user = Db::table('game_user')
                    ->where('uid', $uid)
                    ->where('app_id', $app_id)
                    ->where('user_type', 1)
                    ->find();
                if (!is_array($user) || count($user)<=0)
                {
                    Db::table('game_user')
                        ->insert([
                            'app_id' => $app_id,
                            'uid' => $uid,
                            'real_name' => $real_name,
                            'idcard' => $idcard,
                            'create_time' => time(),
                            'session_id' => $session_id,
                            'update_time' => time(),
                            'online_time' => 0
                        ]);
                }
                // 提交事务
                Db::commit();
                $this->success("实名认证<br />成功", url('Bindprofile/directReturn', [
                    'appId' => $app_id,
                    'uid' => $uid,
                    'sessionId' => $session_id,
                    'deviceId' => $device_id
                ]));
            } catch (\think\Exception $e) {
                // 回滚事务
                Db::rollback();
                $this->error("实名认证<br />失败". $e->getMessage());
            }
        }
        else
        {
            $this->error("只允许<br />POST请求");
        }
    }

    public function directReturn()
    {
        $app_id = $this->request->param("appId", 0, 'intval');
        $app = GameAppModel::get($app_id);
        if (!$app) {
            $this->error("该应用不存在!");
        }
        $uid = $this->request->param("uid");
        if (!$uid) {
            $this->error("uid参数不能为空!");
        }
        $session_id = $this->request->param("sessionId");
        if (!$session_id) {
            $this->error("sessionId参数不能为空!");
        }
        $device_id = $this->request->param("deviceId");
        if (!$device_id) {
            $this->error("deviceId参数不能为空!");
        }

        $manager = new FatigueMgr();

        // 应用的防沉迷状态禁用时
        if ($app->fatigue_status == 0) {
            $this->assign("status", $manager->getNoFatigueStatus());
        } else {
            $user = GameUserModel::get([
                'app_id' => $app_id,
                'uid' => $uid,
                'user_type' => 1
            ]);
            if (!$user) {
                $this->assign('status', $manager->getGuestStatus($app_id, $uid, $device_id, $session_id));
            } else {
                $this->assign('status', $manager->getUserStatus($app_id, $device_id, $uid, $session_id, $user->idcard, $user->real_name));
            }
        }

        $this->assign("app", $app);
        return $this->fetch();
    }
}