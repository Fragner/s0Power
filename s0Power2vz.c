/**************************************************************************
S0/Impulse to Volkszaehler 'RaspberryPI deamon'.
converts the S0 impulse to powervalues
the updatecycle off the middleware is configurable in the config file by updateTime

https://github.com/fragner/s0Power2vz.git
Henrik Wellschmidt  <w3llschmidt@gmail.com>
changed by Martin Fragner <frama1038@gmail.com>
this is a fork from https://github.com/w3llschmid/s0vz.git

**************************************************************************/

#define DAEMON_NAME "s0Power2vz"
#define DAEMON_VERSION "1.0.1-frama"
#define DAEMON_BUILD "4"

/**************************************************************************

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************/

#include <stdio.h>              /* standard library functions for file input and output */
#include <stdlib.h>             /* standard library for the C programming language, */
#include <string.h>             /* functions implementing operations on strings  */
#include <unistd.h>             /* provides access to the POSIX operating system API */
#include <sys/stat.h>           /* declares the stat() functions; umask */
#include <fcntl.h>              /* file descriptors */
#include <syslog.h>             /* send messages to the system logger */
#include <errno.h>              /* macros to report error conditions through error codes */
#include <signal.h>             /* signal processing */
#include <stddef.h>             /* defines the macros NULL and offsetof as well as the types ptrdiff_t, wchar_t, and size_t */

#include <libconfig.h>          /* reading, manipulating, and writing structured configuration files */
#include <curl/curl.h>          /* multiprotocol file transfer library */
#include <poll.h>			/* wait for events on file descriptors */

#include <sys/ioctl.h>		/* */

#include <stdbool.h>

#define BUF_LEN 64

void daemonShutdown();
void signal_handler(int sig);
void daemonize(char *rundir, char *pidfile);

int pidFilehandle, vzport, i, len, running_handles, rc;

const char *vzserver, *vzpath, *vzuuid[64];

//char gpio_pin_id[] = { 17, 18, 27, 22, 23, 24 }, url[128];
char gpio_pin_id[] = {2 }, url[128];

int inputs = sizeof(gpio_pin_id)/sizeof(gpio_pin_id[0]);

struct timeval tv;

CURL *easyhandle[sizeof(gpio_pin_id)/sizeof(gpio_pin_id[0])];
CURLM *multihandle;
CURLMcode multihandle_res;

static char errorBuffer[CURL_ERROR_SIZE+1];

/***********************************************
 * framas changes
*/
time_t m_tStart, m_tEnd;
int m_updateTime = 0; //time setted by config-file
static int cEMPTY = 99999999;
struct timeval m_tv2;
unsigned long long m_ullTStart, m_ullTEnd;


void update_curl_handle_value(const char *vzuuid, int iRun, int iVal);
bool checkTime(void);
int calcPower( int iImpCount);
unsigned long long unixtime_sec(void);
/***********************************************+*/

void signal_handler(int sig) {

	switch(sig)
	{
		case SIGHUP:
		syslog(LOG_WARNING, "Received SIGHUP signal.");
		break;
		case SIGINT:
		case SIGTERM:
		syslog(LOG_INFO, "Daemon exiting");
		daemonShutdown();
		exit(EXIT_SUCCESS);
		break;
		default:
		syslog(LOG_WARNING, "Unhandled signal %s", strsignal(sig));
		break;
	}
}

void daemonShutdown() {
		close(pidFilehandle);
		char pid_file[16];
		sprintf ( pid_file, "/tmp/%s.pid", DAEMON_NAME );
		remove(pid_file);
}

void daemonize(char *rundir, char *pidfile) {
	int pid, sid, i;
	char str[10];
	struct sigaction newSigAction;
	sigset_t newSigSet;

	if (getppid() == 1)
	{
		return;
	}

	sigemptyset(&newSigSet);
	sigaddset(&newSigSet, SIGCHLD);
	sigaddset(&newSigSet, SIGTSTP);
	sigaddset(&newSigSet, SIGTTOU);
	sigaddset(&newSigSet, SIGTTIN);
	sigprocmask(SIG_BLOCK, &newSigSet, NULL);

	newSigAction.sa_handler = signal_handler;
	sigemptyset(&newSigAction.sa_mask);
	newSigAction.sa_flags = 0;

	sigaction(SIGHUP, &newSigAction, NULL);
	sigaction(SIGTERM, &newSigAction, NULL);
	sigaction(SIGINT, &newSigAction, NULL);

	pid = fork();

	if (pid < 0)
	{
		exit(EXIT_FAILURE);
	}

	if (pid > 0)
	{
		printf("Child process created: %d\n", pid);
		exit(EXIT_SUCCESS);
	}	
	umask(027);

	sid = setsid();
	if (sid < 0)
	{
		exit(EXIT_FAILURE);
	}

	for (i = getdtablesize(); i >= 0; --i)
	{
		close(i);
	}

	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);
	chdir(rundir);
	pidFilehandle = open(pidfile, O_RDWR|O_CREAT, 0600);

	if (pidFilehandle == -1 )
	{
		syslog(LOG_INFO, "Could not open PID lock file %s, exiting", pidfile);
		exit(EXIT_FAILURE);
	}

	if (lockf(pidFilehandle,F_TLOCK,0) == -1)
	{
		syslog(LOG_INFO, "Could not lock PID lock file %s, exiting", pidfile);
		exit(EXIT_FAILURE);
	}
	sprintf(str,"%d\n",getpid());
	write(pidFilehandle, str, strlen(str));
}

void cfile() {

	config_t cfg;
	//config_setting_t *setting;
	config_init(&cfg);
	int chdir(const char *path);
	chdir ("/etc");

	if(!config_read_file(&cfg, DAEMON_NAME".cfg"))
	{
		syslog(LOG_INFO, "Config error > /etc/%s - %s\n", config_error_file(&cfg),config_error_text(&cfg));
		config_destroy(&cfg);
		daemonShutdown();
		exit(EXIT_FAILURE);
	}

	if (!config_lookup_string(&cfg, "vzserver", &vzserver))
	{
		syslog(LOG_INFO, "Missing 'VzServer' setting in configuration file.");
		config_destroy(&cfg);
		daemonShutdown();
		exit(EXIT_FAILURE);
	}
	else
	syslog(LOG_INFO, "VzServer:%s", vzserver);

	if (!config_lookup_int(&cfg, "vzport", &vzport))
	{
		syslog(LOG_INFO, "Missing 'VzPort' setting in configuration file.");
		config_destroy(&cfg);
		daemonShutdown();
		exit(EXIT_FAILURE);
	}
	else
	syslog(LOG_INFO, "VzPort:%d", vzport);

	if (!config_lookup_string(&cfg, "vzpath", &vzpath))
	{
		syslog(LOG_INFO, "Missing 'VzPath' setting in configuration file.");
		config_destroy(&cfg);
		daemonShutdown();
		exit(EXIT_FAILURE);
	}
	else
	syslog(LOG_INFO, "VzPath:%s", vzpath);

	for (i=0; i<inputs; i++)
	{
		char gpio[6];
		sprintf ( gpio, "GPIO%01d", i );
		if ( config_lookup_string( &cfg, gpio, &vzuuid[i]) == CONFIG_TRUE )
		syslog ( LOG_INFO, "%s = %s", gpio, vzuuid[i] );
	}
	
	//frama
	if (config_lookup_int(&cfg, "updateTime", &m_updateTime))
	{
		syslog(LOG_INFO, "m_updateTime:%d", m_updateTime);	
	}	
	else syslog(LOG_INFO, "m_updateTime:%d not found", m_updateTime);	
}

unsigned long long unixtime() {
	gettimeofday(&tv,NULL);
	unsigned long long ms_timestamp = (unsigned long long)(tv.tv_sec) * 1000 + (unsigned long long)(tv.tv_usec) / 1000;
return ms_timestamp;
}

void update_curl_handle(const char *vzuuid, int iRun, int iVal) {
		curl_multi_remove_handle(multihandle, easyhandle[iRun]);			
		if (iVal == cEMPTY) {
			sprintf(url, "http://%s:%d/%s/data/%s.json?ts=%llu", vzserver, vzport, vzpath, vzuuid, unixtime());		
		}
		else {			
			sprintf(url, "http://%s:%d/%s/data/%s.json?ts=%llu&value=%d", vzserver, vzport, vzpath, vzuuid, unixtime(), iVal);
		}
		syslog ( LOG_INFO, "send to this url:  %s", url );			
		curl_easy_setopt(easyhandle[iRun], CURLOPT_URL, url);		
		curl_multi_add_handle(multihandle, easyhandle[iRun]);				
}

int main(void) {

	//frama
	int iImpCount [12] = {0,0,0,0};//12 is a test
	iImpCount[0] = 0;
	int iPower, iRun, iTest;	
	//init start time 
	time(&m_tStart);
	m_ullTStart = unixtime_sec();
	//frama
	
	freopen( "/dev/null", "r", stdin);
	freopen( "/dev/null", "w", stdout);
	freopen( "/dev/null", "w", stderr);

	FILE* devnull = NULL;		
	devnull = fopen("/dev/null", "w+");
		
	setlogmask(LOG_UPTO(LOG_INFO));
	openlog(DAEMON_NAME, LOG_CONS | LOG_PERROR, LOG_USER);
	syslog ( LOG_INFO, "S0/Impulse to Volkszaehler RaspberryPI deamon %s.%s", DAEMON_VERSION, DAEMON_BUILD );	
	cfile();	
	char pid_file[16];	
	sprintf ( pid_file, "/tmp/%s.pid", DAEMON_NAME );
	daemonize( "/tmp/", pid_file );	
	char buffer[BUF_LEN];
	struct pollfd fds[inputs];
	
	curl_global_init(CURL_GLOBAL_ALL);
	multihandle = curl_multi_init();	
			
	for (i=0; i<inputs; i++) {		
		snprintf ( buffer, BUF_LEN, "/sys/class/gpio/gpio%d/value", gpio_pin_id[i] );
		if((fds[i].fd = open(buffer, O_RDONLY|O_NONBLOCK)) == 0) {			
			syslog(LOG_INFO,"Error:%s (%m)", buffer);
			exit(1);				
		}
	
		fds[i].events = POLLPRI;
		fds[i].revents = 0;	
			
		easyhandle[i] = curl_easy_init();
		
		curl_easy_setopt(easyhandle[i], CURLOPT_URL, url);
		curl_easy_setopt(easyhandle[i], CURLOPT_POSTFIELDS, "");
		curl_easy_setopt(easyhandle[i], CURLOPT_USERAGENT, DAEMON_NAME " " DAEMON_VERSION );
		curl_easy_setopt(easyhandle[i], CURLOPT_WRITEDATA, devnull);
		curl_easy_setopt(easyhandle[i], CURLOPT_ERRORBUFFER, errorBuffer);
		
		curl_multi_add_handle(multihandle, easyhandle[i]);
									
	}
										
	for ( ;; ) {	
		if((multihandle_res = curl_multi_perform(multihandle, &running_handles)) != CURLM_OK) {
		syslog(LOG_INFO, "HTTP_POST(): %s", curl_multi_strerror(multihandle_res) );
		}
		
		int ret = poll(fds, inputs, 1000);				
		if(ret>0) {
			for (i=0; i<inputs; i++) {
				if (fds[i].revents & POLLPRI) {
					len = read(fds[i].fd, buffer, BUF_LEN);
//					update_curl_handle(vzuuid[i], i, cEMPTY);
					iImpCount[i]++;
//					syslog(LOG_INFO, "counted impulse: %d, Index: %d", iImpCount[i], i);
					iTest++;
					if (iTest >= 100) {
						syslog(LOG_INFO, "%d signal's received, -> still alive ", iTest);//frama
						iTest = 0;
					}
				}
			}
		}
		//frama
		if ((m_updateTime > 0) && checkTime()) {
			for (iRun=0; iRun<inputs; iRun++) {	
				iPower = calcPower(iImpCount[iRun]);
				syslog(LOG_INFO, "counted impulse: %d, calculated Power: %d, Index: %d", iImpCount[iRun], iPower, iRun);						
				update_curl_handle(vzuuid[iRun], iRun, iPower);
				//reset counter
				iImpCount[iRun] = 0;
			}
		}
		//frama					
	}	
	curl_global_cleanup();	
return 0;
}//main_end

/*****************************************
* framas functions
*/

/* powermeter has an resolution from 1000 Imp/kWh */
int calcPower( int iImpCount)	{
	int iPower = 0;
	if (iImpCount > 0) {
		iPower = (3600 * iImpCount)/ m_updateTime;
	}
	return iPower;
}

/*
	check the time difference between the calls
	when the diff is bigger than the time setted in the config file, trigger curl
	input: none
	return: true when the time diff is bigger than the configerd time
*/
bool checkTime (void) {
	int  iDiff;	
	m_ullTEnd = unixtime_sec();	
	iDiff = (int) (m_ullTEnd - m_ullTStart);
//	syslog(LOG_INFO, "Startzeit: %llu, EndZeit: %llu, Differenz : %d",m_ullTStart, m_ullTEnd, iDiff);
	if (iDiff >= m_updateTime)
	{
//		syslog(LOG_INFO, "Es sind %d Sekunden vergangen, --> trigger Curl.", iDiff);
		//init start time 
		m_ullTStart = unixtime_sec();
		return true;
	}
	return false;
}

unsigned long long unixtime_sec() {
	gettimeofday(&m_tv2,NULL);
	return (unsigned long long)(m_tv2.tv_sec);
}
