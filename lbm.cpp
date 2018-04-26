#include <iostream> //输入输出流
#include <cmath>  //数学函数库
#include <cstdlib> //常用的函数 不知道放到哪里函数就放这里面
#include <iomanip> //主要是对cin,cout之类的一些操纵运算子，比如setfill,setw,setbase,setprecision等等 是一种控制文件
#include <fstream> //数据的输入输出 文件流
#include <sstream> //通常用来做数据转换
#include <string>  //string字符串的头文件

using namespace std;

const int Q = 9;		//D2Q9模型 离散速度的总个数9
const int NX = 256;  	//x方向格子数 共有256个
const int NY = 256;		//y方向格子数 共有256个
const double U = 0.1;	//顶盖速度 这里是宏观常量0.1
//#define NUM 5000;

int e[Q][2]={{0,0},{1,0},{0,1},{-1,0},{0,-1},{1,1},{-1,1},{-1,-1},{1,-1}};	//各个方向的离散速度 这是根据D2Q9模型得到的
double w[Q]={4.0/9,1.0/9,1.0/9,1.0/9,1.0/9,1.0/36,1.0/36,1.0/36,1.0/36};	//不同的权系数 通过公式推导算出来的


double rho[NX+1][NY+1];      //密度rou 那么多格点数 总共有+1个节点数
double u[NX+1][NY+1][2];     //n+1时层的速度 
double u0[NX+1][NY+1][2];    //n时层的速度
double f[NX+1][NY+1][Q];     //演化前的分布函数
double F[NX+1][NY+1][Q];     //演化后的分布函数


int i,j,k,ip,jp,n;       //i,j,k 三重for循环的全局变量的定义 每个变量的定义

double c,Re,dx,dy,Lx,Ly,dt,rho0,tau_f,niu,error;    //c是格子速度 Re是雷诺数 dt是时间步长  rho0是流场初始密度 
                                                    //Lx,Ly是宏观的长度    rho0是初始密度  
                                                    //tau_f无量纲松弛时间 niu运动粘度系数 error是两个相邻时层速度的最大相对误差

void init();   //初始化函数

double feq1(int k,double rho,double u[2]);	//计算平衡态分布函数 参数：不同的方向,密度，不同时刻速度

void evolution(); //演化函数

void output(int m);  // 输出函数 把数据输出到.data文件当中

void Error(); //计算误差的函数

int main()  //主函数
{
	init();            //函数的初始化
	for(n=0;;n++)
	{
		evolution();    //调用演化函数
		if(n%1000==0)
		{
			Error();  //每1000次输出一次计算误差
			cout<<"The"<<n<<"th computation result:"<<endl <<"The u,v of point(NX/2,NY/2)is:"<<setprecision(6)<<u[NX/2][NY/2][0]<<","<<u[NX/2][NY/2][1]<<endl;
			cout<<"The max relative error of uv is:"<<setiosflags(ios::scientific)<<error<<endl; //精度是6位 
			if (n>=1000)
			{
				if(n%1000==0)
					output(n);   //输出数据到.dat文件当中
				else if(error<1.0e-6)  //否则 精度达到 退出
					break;
			}
		}
	}
	return 0;
}

//--------------------各个函数的定义------------------------//



void init()                    //初始化函数的定义
{
	dx=1.0;				//格子步长
	dy=1.0;
	Lx=dx*double(NY);	//宏观的方腔尺寸
	Ly=dy*double(NX);
	dt=dx;				//时间步长
	c=dx/dt;			//1.0，格子速度  在使用迁移碰撞的标准格子boltzmann方法中，为保证粒子在格子上运动，在空间步长和时间步长为1，即c=1
	rho0=1.0;			//初始密度为1
	Re=100;			//雷诺数Re=kMa/Kn，式中Ma为马赫数；Kn为克努曾数；k为常数。流动速度很高，雷诺数和马赫数都起着重要作用。如果空气稀薄，则克努曾数起着主要作用。
	
	
	niu=U*Lx/Re;		//运动黏度系数 这个公式没找到
	tau_f=3.0*niu+0.5;	//无量纲松弛时间 
	cout<<"tau_f="<<tau_f<<endl;

	for(i=0;i<=NX;i++)	//接下来对每一个格子进行初始化
		for(j=0;j<=NY;j++)
		{
			u[i][j][0]=0;      //初始化为0
			u[i][j][1]=0;      //初始化为0
			rho[i][j]=rho0;    //初始化为0
			u[i][NY][0]=U;     //最上层的速度为宏观流速U=0.1
			for(k=0;k<Q;k++)    //在9个方向上分别调用平衡态分布函数feq1
			{
				f[i][j][k]=feq1(k,rho[i][j],u[i][j]);   //调用平衡态函数feq1
			}
		}
}

double feq1(int k,double rho,double u[2])	//计算平衡态分布函数
{
	double eu,uv,feq;             //定义了三个变量，eu=e()*u,u是气体的宏观流动速度,uv   feq是得到的值
	eu=(e[k][0]*u[0]+e[k][1]*u[1]);    //速度空间的每个元素*速度0
	uv=(u[0]*u[0]+u[1]*u[1]);      //自己和自己相乘
	feq=w[k]*rho*(1.0+3.0*eu+4.5*eu*eu-1.5*uv);  //平衡态分布函数 rho是初始密度，这里取的是1，w[k]是权系数，PPT第14页的公式
	return feq;                          //tau_f>0.5
}

void evolution()     
{
	for(i=1;i<NX;i++)	//演化函数
		for(j=1;j<NY;j++)
			for(k=0;k<Q;k++)
			{
				ip=i-e[k][0];
				jp=j-e[k][1];
				F[i][j][k]=f[ip][jp][k]+(feq1(k,rho[ip][jp],u[ip][jp])-f[ip][jp][k])/tau_f; //利用前面的演化方程进行计算 PPT第7页的演化方程
			}                                                              //右端为碰撞项 tau_f是无量纲单松弛时间，用来控制f趋向于feq的速率 

	for(i=1;i<NX;i++)	//计算宏观量
		for(j=1;j<NY;j++)
		{
			u0[i][j][0]=u[i][j][0];
			u0[i][j][1]=u[i][j][1];
			rho[i][j]=0;
			u[i][j][0]=0;
			u[i][j][1]=0;
			for(k=0;k<Q;k++)           //分别计算9个方向上的速度
			{
				f[i][j][k]=F[i][j][k];               //？
				rho[i][j]+=f[i][j][k];          //格子 Boltzmann 方法中宏观的物理量满足的距方程，可以用它来计算宏观量。    
				u[i][j][0]+=e[k][0]*f[i][j][k]; //
				u[i][j][1]+=e[k][1]*f[i][j][k]; //
			}
			u[i][j][0]/=rho[i][j];      //公式里面有个rho 除去
			u[i][j][1]/=rho[i][j];        //
		}


	//边界处理 二阶精度  采用的是非平衡态外推格式？将边界节点的分布函数分解为 平衡态和非平衡态 
    //平衡态部分有边界条件的定义近似获得 非平衡态的部分则有非平衡态外推确定
	for(j=1;j<NY;j++)		//左右边界
		for(k=0;k<Q;k++)
		{
			rho[NX][j]=rho[NX-1][j];  //密度按往里面的一层，计算
			f[NX][j][k]=feq1(k,rho[NX][j],u[NX][j])+f[NX-1][j][k]-feq1(k,rho[NX-1][j],u[NX-1][j]); //最右边的边界节点的分布函数可以由以下式子获得
			rho[0][j]=rho[1][j];  //也是往里面一层进行计算
			f[0][j][k]=feq1(k,rho[0][j],u[0][j])+f[1][j][k]-feq1(k,rho[1][j],u[1][j]); //最左边的边界节点计算公式如下
		}

	for(i=0;i<NX;i++)      //上下边界的计算公式 
		for(k=0;k<Q;k++)     
		{
			rho[i][0]=rho[i][1];
			f[i][0][k]=feq1(k,rho[i][0],u[i][0])+f[i][1][k]-feq1(k,rho[i][1],u[i][1]); //最下面的计算边界的计算公式 也是按照PPT20页的公式计算
			rho[i][NY]=rho[i][NY-1];
			u[i][NY][0]=U;    //最上面的就让它的速度等于宏观流速
			f[i][NY][k]=feq1(k,rho[i][NY],u[i][NY])+f[i][NY-1][k]-feq1(k,rho[i][NY-1],u[i][NY-1]);//计算
		}
}

void output(int m)	//输出数据到cavity_m.data
{
	ostringstream filename;                     //定义文件名 
	filename<<"cavity_"<<m<<".dat";
	ofstream fout(filename.str().c_str());   // fout
	fout<<"Title=\"LBM Lid Driven Flow\"\n"<<"VARIABLES=\"X\",\"Y\",\"U\",\"V\"\n"<<"ZONE T=\"BOX\",I="<<NX+1<<",J="<<NY+1<<",F=POINT"<<endl;
	for(j=0;j<=NY;j++)
		for(i=0;i<=NX;i++)
		{
			fout<<double(i)/Lx<<" "<<double(j)/Ly<<" "<<u[i][j][0]<<" "<<u[i][j][1]<<endl;
		}
}

void Error()          //最大相对误差的计算函数
{
	double temp1=0;
	double temp2=0;

	for(i=0;i<NX;i++)
		for(j=0;j<NY;j++)
		{
			temp1 += ((u[i][j][0]-u0[i][j][0])*(u[i][j][0]-u0[i][j][0])+(u[i][j][1]-u0[i][j][1])*(u[i][j][1]-u0[i][j][1]));
			temp2 += (u[i][j][0]*u[i][j][0]+u[i][j][1]*u[i][j][1]);
		}
	temp1=sqrt(temp1);
	temp2=sqrt(temp2);
	error=temp1/(temp2+1e-30);
}