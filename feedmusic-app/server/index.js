const express = require('express');
const cors = require('cors');
const app = express();
const port = 5005;

// 中间件
app.use(cors());
app.use(express.json());

// 模拟数据库
let users = [
  { id: 1, username: 'admin', password: 'admin123' },
  { id: 2, username: 'user1', password: 'user123' }
];

let news = [
  {
    id: 1,
    title: 'FeedMusic 推出全新音乐体验',
    description: '我们很高兴地宣布推出全新的音乐体验，带来更好的音质和更多的音乐选择。无论你喜欢什么类型的音乐，都能在这里找到适合你的内容。',
    image: '1d920bfa-a07e-4656-a795-4601c24f6504.png',
    author: 'admin',
    createdAt: new Date('2023-06-15')
  },
  {
    id: 2,
    title: '夏季音乐节即将开始',
    description: '一年一度的夏季音乐节将于下月开始，众多知名音乐人将登台表演。提前购票可享受早鸟优惠，不要错过这个音乐盛宴。',
    image: 'presentation-background.jpg',
    author: 'user1',
    createdAt: new Date('2023-06-10')
  },
  {
    id: 3,
    title: '全新推荐算法上线',
    description: '我们更新了音乐推荐算法，将根据你的听歌习惯提供更精准的音乐推荐。现在开始，发现更多你喜欢的音乐。',
    image: 'start-music-background.jpg',
    author: 'admin',
    createdAt: new Date('2023-06-05')
  },
  {
    id: 4,
    title: 'FeedMusic 移动应用更新',
    description: '我们的移动应用迎来重大更新，新增了多项实用功能，包括离线下载、歌词显示等。立即更新体验全新功能。',
    image: '1d920bfa-a07e-4656-a795-4601c24f6504.png',
    author: 'user1',
    createdAt: new Date('2023-05-28')
  },
  {
    id: 5,
    title: '与知名唱片公司达成合作',
    description: 'FeedMusic 正式与多家知名唱片公司达成合作，将独家推出更多热门专辑。用户可以第一时间收听到最新音乐。',
    image: 'presentation-background.jpg',
    author: 'admin',
    createdAt: new Date('2023-05-20')
  },
  {
    id: 6,
    title: '音乐创作大赛开始报名',
    description: '第一届 FeedMusic 音乐创作大赛正式开始报名，无论你是专业音乐人还是音乐爱好者，都可以参与其中，赢取丰厚奖品。',
    image: 'start-music-background.jpg',
    author: 'admin',
    createdAt: new Date('2023-05-15')
  },
  {
    id: 7,
    title: '新用户专享福利活动',
    description: '为了欢迎新用户，我们推出了专享福利活动，新注册用户可获得30天 premium 会员体验，享受无广告、高品质音乐等特权。',
    image: '1d920bfa-a07e-4656-a795-4601c24f6504.png',
    author: 'user1',
    createdAt: new Date('2023-05-10')
  },
  {
    id: 8,
    title: 'FeedMusic 社区功能上线',
    description: '我们很高兴地宣布社区功能正式上线，用户可以在社区中分享自己喜欢的音乐，结识志同道合的音乐爱好者。',
    image: 'presentation-background.jpg',
    author: 'admin',
    createdAt: new Date('2023-05-05')
  },
  {
    id: 9,
    title: '音质提升计划完成',
    description: '经过数月的努力，我们的音质提升计划已经完成，现在所有音乐都支持高清音质播放，为你带来身临其境的听觉体验。',
    image: 'start-music-background.jpg',
    author: 'user1',
    createdAt: new Date('2023-04-30')
  }
];

// 认证相关 API
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);
  
  if (user) {
    // 模拟 JWT token
    const token = `token_${user.id}`;
    res.json({ 
      success: true, 
      token, 
      user: { id: user.id, username: user.username } 
    });
  } else {
    res.json({ success: false, message: '用户名或密码错误' });
  }
});

app.post('/api/register', (req, res) => {
  const { username, password } = req.body;
  const existingUser = users.find(u => u.username === username);
  
  if (existingUser) {
    return res.json({ success: false, message: '用户名已存在' });
  }
  
  const newUser = {
    id: users.length + 1,
    username,
    password
  };
  
  users.push(newUser);
  
  res.json({ 
    success: true, 
    user: { id: newUser.id, username: newUser.username } 
  });
});

app.get('/api/auth/status', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.json({ isAuthenticated: false });
  }
  
  // 从 token 中解析用户 ID
  const userId = parseInt(token.split('_')[1]);
  const user = users.find(u => u.id === userId);
  
  if (user) {
    res.json({ 
      isAuthenticated: true, 
      user: { id: user.id, username: user.username } 
    });
  } else {
    res.json({ isAuthenticated: false });
  }
});

// 新闻相关 API
app.get('/api/news', (req, res) => {
  res.json(news);
});

app.get('/api/news/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const item = news.find(n => n.id === id);
  
  if (item) {
    res.json(item);
  } else {
    res.status(404).json({ message: '新闻不存在' });
  }
});

app.post('/api/admin/news', (req, res) => {
  // 简单的权限检查
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ message: '未授权' });
  }
  
  const userId = parseInt(token.split('_')[1]);
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(401).json({ message: '未授权' });
  }
  
  const newNews = {
    id: news.length + 1,
    ...req.body,
    author: user.username,
    createdAt: new Date()
  };
  
  news.push(newNews);
  res.json(newNews);
});

app.put('/api/admin/news/:id', (req, res) => {
  // 简单的权限检查
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ message: '未授权' });
  }
  
  const userId = parseInt(token.split('_')[1]);
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(401).json({ message: '未授权' });
  }
  
  const id = parseInt(req.params.id);
  const index = news.findIndex(n => n.id === id);
  
  if (index === -1) {
    return res.status(404).json({ message: '新闻不存在' });
  }
  
  news[index] = {
    ...news[index],
    ...req.body,
    updatedAt: new Date()
  };
  
  res.json(news[index]);
});

app.delete('/api/admin/news/:id', (req, res) => {
  // 简单的权限检查
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ message: '未授权' });
  }
  
  const userId = parseInt(token.split('_')[1]);
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(401).json({ message: '未授权' });
  }
  
  const id = parseInt(req.params.id);
  const initialLength = news.length;
  news = news.filter(n => n.id !== id);
  
  if (news.length < initialLength) {
    res.json({ success: true });
  } else {
    res.status(404).json({ message: '新闻不存在' });
  }
});

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});
