interface VideoPlayerProps {
  videoId: number
}

export default function VideoPlayer({ videoId }: VideoPlayerProps) {
  const streamUrl = `/api/videos/${videoId}/stream`
  const thumbUrl = `/api/videos/${videoId}/thumbnail`

  return (
    <div className="aspect-[9/16] max-h-[70vh] bg-black rounded-lg overflow-hidden">
      <video
        key={videoId}
        src={streamUrl}
        poster={thumbUrl}
        controls
        autoPlay
        className="w-full h-full object-contain"
        onError={(e) => {
          const target = e.target as HTMLVideoElement
          target.poster = ''
        }}
      >
        Your browser does not support the video tag.
      </video>
    </div>
  )
}
