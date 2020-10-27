/*
*      Copyright (C) 2005-2013 Team XBMC
*      http://xbmc.org
*
*  This Program is free software; you can redistribute it and/or modify
*  it under the terms of the GNU General Public License as published by
*  the Free Software Foundation; either version 2, or (at your option)
*  any later version.
*
*  This Program is distributed in the hope that it will be useful,
*  but WITHOUT ANY WARRANTY; without even the implied warranty of
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
*  GNU General Public License for more details.
*
*  You should have received a copy of the GNU General Public License
*  along with XBMC; see the file COPYING.  If not, see
*  <http://www.gnu.org/licenses/>.
*
*/

#include "system.h"
#include "Splash.h"
#include "guiImage.h"
#include "FileSystem/File.h"
#include "settings/AdvancedSettings.h"
#include "settings/GUISettings.h"
#include "interfaces/Builtins.h"
#include "GUIInfoManager.h"
#include "utils/URIUtils.h"
#include "FileSystem/SpecialProtocol.h"
#include "log.h"

using namespace XFILE;

CSplash::CSplash(const CStdString& imageName)
{
	m_ImageName = imageName;
}

CSplash::~CSplash()
{
	Stop();
}

void CSplash::OnStartup()
{}

void CSplash::OnExit()
{}

void CSplash::Process()
{
	D3DGAMMARAMP newRamp;
	D3DGAMMARAMP oldRamp;

	g_graphicsContext.Lock();
	g_graphicsContext.Get3DDevice()->Clear(0, NULL, D3DCLEAR_TARGET, 0, 0, 0);

	g_graphicsContext.SetCameraPosition(CPoint(0, 0));
	float w = g_graphicsContext.GetWidth();
	float h = g_graphicsContext.GetHeight();
	// Store the old gamma ramp
	g_graphicsContext.Get3DDevice()->GetGammaRamp(&oldRamp);
	float fade = 0.5f;
	for (int i = 0; i < 256; i++)
	{
		newRamp.red[i] = (int)((float)oldRamp.red[i] * fade);
		newRamp.green[i] = (int)((float)oldRamp.red[i] * fade);
		newRamp.blue[i] = (int)((float)oldRamp.red[i] * fade);
	}
	g_graphicsContext.Get3DDevice()->SetGammaRamp(GAMMA_RAMP_FLAG, &newRamp);
	//render splash image
#ifndef HAS_XBOX_D3D
	g_graphicsContext.Get3DDevice()->BeginScene();
#endif
	if (!CFile::Exists(m_ThemeSplash) && !CFile::Exists(m_CustomSplash))
	{
		CGUIImage* image = new CGUIImage(0, 0, 0, 0, w, h, m_ImageName);
		image->SetAspectRatio(CAspectRatio::AR_STRETCH);
		image->AllocResources();
		image->Render();
		image->FreeResources();
		delete image;
	}
	if (CFile::Exists(m_ThemeSplash) && !CFile::Exists(m_CustomSplash))
	{
		CGUIImage* imagetheme = new CGUIImage(0, 0, 0, 0, w, h, m_ThemeSplash);
		imagetheme->SetAspectRatio(CAspectRatio::AR_STRETCH);
		imagetheme->AllocResources();
		imagetheme->Render();
		imagetheme->FreeResources();
		delete imagetheme;
	}
	if (CFile::Exists(m_CustomSplash))
	{
		CGUIImage* imagecustom = new CGUIImage(0, 0, 0, 0, w, h, m_CustomSplash);
		imagecustom->SetAspectRatio(CAspectRatio::AR_STRETCH);
		imagecustom->AllocResources();
		imagecustom->Render();
		imagecustom->FreeResources();
		delete imagecustom;
	}
	//show it on screen
#ifdef HAS_XBOX_D3D
	g_graphicsContext.Get3DDevice()->BlockUntilVerticalBlank();
#else
	g_graphicsContext.Get3DDevice()->EndScene();
#endif
	g_graphicsContext.Get3DDevice()->Present( NULL, NULL, NULL, NULL );
	g_graphicsContext.Unlock();

	//fade in and wait untill the thread is stopped
	while (!m_bStop)
	{
		if (fade <= 1.f)
		{
			for (int i = 0; i < 256; i++)
			{
				newRamp.red[i] = (int)((float)oldRamp.red[i] * fade);
				newRamp.green[i] = (int)((float)oldRamp.green[i] * fade);
				newRamp.blue[i] = (int)((float)oldRamp.blue[i] * fade);
			}
			g_graphicsContext.Lock();
			Sleep(3);
			g_graphicsContext.Get3DDevice()->SetGammaRamp(GAMMA_RAMP_FLAG, &newRamp);
			g_graphicsContext.Unlock();
			fade += 0.01f;
		}
		else
		{
			Sleep(10);
		}
	}

	g_graphicsContext.Lock();
	// fade out
	for (float fadeout = fade - 0.01f; fadeout >= 0.f; fadeout -= 0.01f)
	{
		for (int i = 0; i < 256; i++)
		{
			newRamp.red[i] = (int)((float)oldRamp.red[i] * fadeout);
			newRamp.green[i] = (int)((float)oldRamp.green[i] * fadeout);
			newRamp.blue[i] = (int)((float)oldRamp.blue[i] * fadeout);
		}
		Sleep(3);
		g_graphicsContext.Get3DDevice()->SetGammaRamp(GAMMA_RAMP_FLAG, &newRamp);
	}
	//restore original gamma ramp
	g_graphicsContext.Get3DDevice()->Clear(0, NULL, D3DCLEAR_TARGET, 0, 0, 0);
	g_graphicsContext.Get3DDevice()->SetGammaRamp(0, &oldRamp);
	g_graphicsContext.Get3DDevice()->Present( NULL, NULL, NULL, NULL );
	g_graphicsContext.Unlock();
}

bool CSplash::Start()
{
	if (!g_advancedSettings.m_splashImage)
	{
		CLog::Log(LOGDEBUG, "Splash disabled");
		return false;
	}
	if (g_infoManager.GetBool(g_infoManager.TranslateString("skin.hassetting(introenabled)")) == 1)
	{
		CLog::Log(LOGDEBUG, "Splash disabled due to intro being enabled.");
		return false;
	}
	if (g_infoManager.GetBool(g_infoManager.TranslateString("skin.hassetting(randomtheme)")) == 1)
	{
		return false;
	}
	m_ThemeSplash = "Special://root/skins/"+g_guiSettings.GetString("lookandfeel.skin")+"/extras/themes/splashes/"+URIUtils::ReplaceExtension(g_guiSettings.GetString("lookandfeel.skintheme"), ".png");
	// CLog::Log(LOGNOTICE, m_ThemeSplash.c_str());
	m_CustomSplash = "Special://root/custom_splash.png";
	Create();
	Sleep(3000);
	return true;
}

void CSplash::Stop()
{
	StopThread();
}

bool CSplash::IsRunning()
{
	return (m_ThreadHandle != NULL);
}
