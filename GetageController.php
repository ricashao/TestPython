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

namespace api\realname\controller;

use app\realname\model\GameAppModel;
use app\realname\model\GameUserModel;
use util\IDCardMgr;
use cmf\controller\RestBaseController;
use think\Db;

class GetageController extends RestBaseController
{
    public function index()
    {
        $data = $this->request->param();
        if (empty($data['appId']) || empty($data['uid']))
        {
            $this->error('请求参数不完整',$data);
        }

        $appId = $data['appId'];
        $uid = $data['uid'];

       
        $app = GameAppModel::get($appId);
        if (!$app) {
            $this->error("该应用不存在！");
        }
        $user = GameUserModel::get([
            'app_id' => $appId,
            'uid' => $uid,
            'user_type' => 1
        ]);
        if (!$user) {
            $this->error("实名认证玩家不存在！");
        }else
        {
            $this->success('成功', $this->ageLevel($user->idcard));
        }

    }

     /**
     * 判断年龄阶段
     *
     * @param  string $idCard
     * @return string 0:8岁以下, 1:8-15岁, 2:16-17岁, 3:成年人
     */
    private function ageLevel($idCard)
    {
        $manager = new IDCardMgr();
        $age = $manager->age($idCard);
        if ($age < 8)
        {
            // 8岁以下
            return '0';
        }
        else if ($age >=8 && $age < 16)
        {
            // 8-15岁
            return '1';
        }
        else if ($age >=16 && $age < 18)
        {
            // 16-17岁
            return '2';
        }
        else
        {
            // 成年人
            return '3';
        }
    }
}
