import { useEffect, useRef, useCallback } from 'react'
import { useQueryClient } from '@tanstack/react-query'

interface WsEvent {
  event: string
  data: Record<string, unknown>
  timestamp: string
}

export function useWebSocket() {
  const ws = useRef<WebSocket | null>(null)
  const qc = useQueryClient()

  const connect = useCallback(() => {
    const wsUrl = import.meta.env.VITE_WS_URL || `ws://${window.location.host}/ws`
    ws.current = new WebSocket(wsUrl)

    ws.current.onmessage = (event) => {
      try {
        const msg: WsEvent = JSON.parse(event.data)
        switch (msg.event) {
          case 'video_ready':
          case 'video_approved':
          case 'video_rejected':
            qc.invalidateQueries({ queryKey: ['videos'] })
            break
          case 'published':
            qc.invalidateQueries({ queryKey: ['videos'] })
            qc.invalidateQueries({ queryKey: ['analytics'] })
            break
          case 'job_started':
          case 'job_done':
          case 'job_failed':
            qc.invalidateQueries({ queryKey: ['schedule'] })
            break
        }
      } catch {
        // ignore parse errors
      }
    }

    ws.current.onclose = () => {
      setTimeout(connect, 3000) // reconnect after 3s
    }
  }, [qc])

  useEffect(() => {
    connect()
    return () => ws.current?.close()
  }, [connect])
}
