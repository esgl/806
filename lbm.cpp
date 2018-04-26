#include <iostream> //���������
#include <cmath>  //��ѧ������
#include <cstdlib> //���õĺ��� ��֪���ŵ����ﺯ���ͷ�������
#include <iomanip> //��Ҫ�Ƕ�cin,cout֮���һЩ���������ӣ�����setfill,setw,setbase,setprecision�ȵ� ��һ�ֿ����ļ�
#include <fstream> //���ݵ�������� �ļ���
#include <sstream> //ͨ������������ת��
#include <string>  //string�ַ�����ͷ�ļ�

using namespace std;

const int Q = 9;		//D2Q9ģ�� ��ɢ�ٶȵ��ܸ���9
const int NX = 256;  	//x��������� ����256��
const int NY = 256;		//y��������� ����256��
const double U = 0.1;	//�����ٶ� �����Ǻ�۳���0.1
//#define NUM 5000;

int e[Q][2]={{0,0},{1,0},{0,1},{-1,0},{0,-1},{1,1},{-1,1},{-1,-1},{1,-1}};	//�����������ɢ�ٶ� ���Ǹ���D2Q9ģ�͵õ���
double w[Q]={4.0/9,1.0/9,1.0/9,1.0/9,1.0/9,1.0/36,1.0/36,1.0/36,1.0/36};	//��ͬ��Ȩϵ�� ͨ����ʽ�Ƶ��������


double rho[NX+1][NY+1];      //�ܶ�rou ��ô������ �ܹ���+1���ڵ���
double u[NX+1][NY+1][2];     //n+1ʱ����ٶ� 
double u0[NX+1][NY+1][2];    //nʱ����ٶ�
double f[NX+1][NY+1][Q];     //�ݻ�ǰ�ķֲ�����
double F[NX+1][NY+1][Q];     //�ݻ���ķֲ�����


int i,j,k,ip,jp,n;       //i,j,k ����forѭ����ȫ�ֱ����Ķ��� ÿ�������Ķ���

double c,Re,dx,dy,Lx,Ly,dt,rho0,tau_f,niu,error;    //c�Ǹ����ٶ� Re����ŵ�� dt��ʱ�䲽��  rho0��������ʼ�ܶ� 
                                                    //Lx,Ly�Ǻ�۵ĳ���    rho0�ǳ�ʼ�ܶ�  
                                                    //tau_f�������ɳ�ʱ�� niu�˶�ճ��ϵ�� error����������ʱ���ٶȵ����������

void init();   //��ʼ������

double feq1(int k,double rho,double u[2]);	//����ƽ��̬�ֲ����� ��������ͬ�ķ���,�ܶȣ���ͬʱ���ٶ�

void evolution(); //�ݻ�����

void output(int m);  // ������� �����������.data�ļ�����

void Error(); //�������ĺ���

int main()  //������
{
	init();            //�����ĳ�ʼ��
	for(n=0;;n++)
	{
		evolution();    //�����ݻ�����
		if(n%1000==0)
		{
			Error();  //ÿ1000�����һ�μ������
			cout<<"The"<<n<<"th computation result:"<<endl <<"The u,v of point(NX/2,NY/2)is:"<<setprecision(6)<<u[NX/2][NY/2][0]<<","<<u[NX/2][NY/2][1]<<endl;
			cout<<"The max relative error of uv is:"<<setiosflags(ios::scientific)<<error<<endl; //������6λ 
			if (n>=1000)
			{
				if(n%1000==0)
					output(n);   //������ݵ�.dat�ļ�����
				else if(error<1.0e-6)  //���� ���ȴﵽ �˳�
					break;
			}
		}
	}
	return 0;
}

//--------------------���������Ķ���------------------------//



void init()                    //��ʼ�������Ķ���
{
	dx=1.0;				//���Ӳ���
	dy=1.0;
	Lx=dx*double(NY);	//��۵ķ�ǻ�ߴ�
	Ly=dy*double(NX);
	dt=dx;				//ʱ�䲽��
	c=dx/dt;			//1.0�������ٶ�  ��ʹ��Ǩ����ײ�ı�׼����boltzmann�����У�Ϊ��֤�����ڸ������˶����ڿռ䲽����ʱ�䲽��Ϊ1����c=1
	rho0=1.0;			//��ʼ�ܶ�Ϊ1
	Re=100;			//��ŵ��Re=kMa/Kn��ʽ��MaΪ�������KnΪ��Ŭ������kΪ�����������ٶȺܸߣ���ŵ�����������������Ҫ���á��������ϡ�������Ŭ����������Ҫ���á�
	
	
	niu=U*Lx/Re;		//�˶���ϵ�� �����ʽû�ҵ�
	tau_f=3.0*niu+0.5;	//�������ɳ�ʱ�� 
	cout<<"tau_f="<<tau_f<<endl;

	for(i=0;i<=NX;i++)	//��������ÿһ�����ӽ��г�ʼ��
		for(j=0;j<=NY;j++)
		{
			u[i][j][0]=0;      //��ʼ��Ϊ0
			u[i][j][1]=0;      //��ʼ��Ϊ0
			rho[i][j]=rho0;    //��ʼ��Ϊ0
			u[i][NY][0]=U;     //���ϲ���ٶ�Ϊ�������U=0.1
			for(k=0;k<Q;k++)    //��9�������Ϸֱ����ƽ��̬�ֲ�����feq1
			{
				f[i][j][k]=feq1(k,rho[i][j],u[i][j]);   //����ƽ��̬����feq1
			}
		}
}

double feq1(int k,double rho,double u[2])	//����ƽ��̬�ֲ�����
{
	double eu,uv,feq;             //����������������eu=e()*u,u������ĺ�������ٶ�,uv   feq�ǵõ���ֵ
	eu=(e[k][0]*u[0]+e[k][1]*u[1]);    //�ٶȿռ��ÿ��Ԫ��*�ٶ�0
	uv=(u[0]*u[0]+u[1]*u[1]);      //�Լ����Լ����
	feq=w[k]*rho*(1.0+3.0*eu+4.5*eu*eu-1.5*uv);  //ƽ��̬�ֲ����� rho�ǳ�ʼ�ܶȣ�����ȡ����1��w[k]��Ȩϵ����PPT��14ҳ�Ĺ�ʽ
	return feq;                          //tau_f>0.5
}

void evolution()     
{
	for(i=1;i<NX;i++)	//�ݻ�����
		for(j=1;j<NY;j++)
			for(k=0;k<Q;k++)
			{
				ip=i-e[k][0];
				jp=j-e[k][1];
				F[i][j][k]=f[ip][jp][k]+(feq1(k,rho[ip][jp],u[ip][jp])-f[ip][jp][k])/tau_f; //����ǰ����ݻ����̽��м��� PPT��7ҳ���ݻ�����
			}                                                              //�Ҷ�Ϊ��ײ�� tau_f�������ٵ��ɳ�ʱ�䣬��������f������feq������ 

	for(i=1;i<NX;i++)	//��������
		for(j=1;j<NY;j++)
		{
			u0[i][j][0]=u[i][j][0];
			u0[i][j][1]=u[i][j][1];
			rho[i][j]=0;
			u[i][j][0]=0;
			u[i][j][1]=0;
			for(k=0;k<Q;k++)           //�ֱ����9�������ϵ��ٶ�
			{
				f[i][j][k]=F[i][j][k];               //��
				rho[i][j]+=f[i][j][k];          //���� Boltzmann �����к�۵�����������ľ෽�̣���������������������    
				u[i][j][0]+=e[k][0]*f[i][j][k]; //
				u[i][j][1]+=e[k][1]*f[i][j][k]; //
			}
			u[i][j][0]/=rho[i][j];      //��ʽ�����и�rho ��ȥ
			u[i][j][1]/=rho[i][j];        //
		}


	//�߽紦�� ���׾���  ���õ��Ƿ�ƽ��̬���Ƹ�ʽ�����߽�ڵ�ķֲ������ֽ�Ϊ ƽ��̬�ͷ�ƽ��̬ 
    //ƽ��̬�����б߽������Ķ�����ƻ�� ��ƽ��̬�Ĳ������з�ƽ��̬����ȷ��
	for(j=1;j<NY;j++)		//���ұ߽�
		for(k=0;k<Q;k++)
		{
			rho[NX][j]=rho[NX-1][j];  //�ܶȰ��������һ�㣬����
			f[NX][j][k]=feq1(k,rho[NX][j],u[NX][j])+f[NX-1][j][k]-feq1(k,rho[NX-1][j],u[NX-1][j]); //���ұߵı߽�ڵ�ķֲ���������������ʽ�ӻ��
			rho[0][j]=rho[1][j];  //Ҳ��������һ����м���
			f[0][j][k]=feq1(k,rho[0][j],u[0][j])+f[1][j][k]-feq1(k,rho[1][j],u[1][j]); //����ߵı߽�ڵ���㹫ʽ����
		}

	for(i=0;i<NX;i++)      //���±߽�ļ��㹫ʽ 
		for(k=0;k<Q;k++)     
		{
			rho[i][0]=rho[i][1];
			f[i][0][k]=feq1(k,rho[i][0],u[i][0])+f[i][1][k]-feq1(k,rho[i][1],u[i][1]); //������ļ���߽�ļ��㹫ʽ Ҳ�ǰ���PPT20ҳ�Ĺ�ʽ����
			rho[i][NY]=rho[i][NY-1];
			u[i][NY][0]=U;    //������ľ��������ٶȵ��ں������
			f[i][NY][k]=feq1(k,rho[i][NY],u[i][NY])+f[i][NY-1][k]-feq1(k,rho[i][NY-1],u[i][NY-1]);//����
		}
}

void output(int m)	//������ݵ�cavity_m.data
{
	ostringstream filename;                     //�����ļ��� 
	filename<<"cavity_"<<m<<".dat";
	ofstream fout(filename.str().c_str());   // fout
	fout<<"Title=\"LBM Lid Driven Flow\"\n"<<"VARIABLES=\"X\",\"Y\",\"U\",\"V\"\n"<<"ZONE T=\"BOX\",I="<<NX+1<<",J="<<NY+1<<",F=POINT"<<endl;
	for(j=0;j<=NY;j++)
		for(i=0;i<=NX;i++)
		{
			fout<<double(i)/Lx<<" "<<double(j)/Ly<<" "<<u[i][j][0]<<" "<<u[i][j][1]<<endl;
		}
}

void Error()          //���������ļ��㺯��
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